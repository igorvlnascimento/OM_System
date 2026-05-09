import datetime
from pathlib import Path
import random
import time
import hydra
import mlflow
import numpy as np
from omegaconf import DictConfig
import torch

from stage.candidate_generation.candidate_generation import CandidateGeneration
from stage.evaluation.evaluation import Evaluation
from stage.matching.matching import Matching
from stage.postprocessing.postprocessing import Postprocessing
from stage.modularization.modularizer import PageRankModularizer, PPRModularizer, SampleModularizer
from stage.preprocessing.preprocessing import Preprocessing
from stage.verbalization.build_verbalizer import BuildVerbalizer
from stage.verbalization.text_string_verbalizer import TextStringVerbalizer

CURRENT = Path(__file__).resolve()
PROJECT_ROOT = ""

for parent in CURRENT.parents:
    if (parent / "pyproject.toml").exists():
        PROJECT_ROOT = parent
        break


def set_seed(seed: int = 42):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


class OMPipeline:
    """Execute the full ontology matching pipeline for a single ontology pair
    and a single seed.

    The caller is responsible for:
    - Setting up the MLflow experiment and opening the parent run.
    - Iterating over multiple pairs / seeds (see run_grid.py).

    Usage::

        pipeline = OMPipeline(cfg)
        metrics = pipeline.run(seed=42)
        # metrics = {"precision": ..., "recall": ..., "f1": ...}
    """

    def __init__(self, config: DictConfig):
        self.config = config
        self.seed: int | None = None
        self.source_concept_dict: dict = {}
        self.target_concept_dict: dict = {}
        self.final_result = None
        self._metrics: dict[str, float] = {}

    def run(self, seed: int) -> dict[str, float]:
        """Run the pipeline for the pair defined in *config* and the given *seed*.

        Logs metrics and artifacts to the currently active MLflow run.
        Returns a dict with keys ``precision``, ``recall``, ``f1``.
        """
        set_seed(seed)
        self.seed = seed
        self._run_single_pair_pipeline()
        return dict(self._metrics)

    # ── Internal orchestration ─────────────────────────────────────────────────

    def _run_single_pair_pipeline(self) -> None:
        source_modules, target_modules, sample_target_subgraph = self._run_preprocessing()

        source_modules_verbalized, source_verbalizer = self._run_verbalizer(
            source_modules,
            self.config.verbalizer_type.candidate_generator,
            self.config.dataset_name,
            self.config.ontology_source_name,
        )
        target_modules_verbalized, target_verbalizer = self._run_verbalizer(
            target_modules,
            self.config.verbalizer_type.candidate_generator,
            self.config.dataset_name,
            self.config.ontology_target_name,
        )

        candidates = self._run_candidate_gen(
            source_modules_verbalized,
            target_modules_verbalized,
            self.preprocessing.ontology_target_path,
            sample_target_subgraph,
        )

        source_verbalized = [source for source, _ in candidates]
        target_modules = [target for _, target in candidates]
        target_verbalized, _ = self._run_verbalizer(
            target_modules,
            self.config.verbalizer_type.matcher,
            self.config.dataset_name,
            self.config.ontology_target_name,
        )

        self.source_concept_dict = source_verbalizer.concept_dict
        self.target_concept_dict = target_verbalizer.concept_dict

        outputs = self._run_matching((source_verbalized, target_verbalized))
        predicted_edoal = self._run_postprocessing(outputs)
        self._run_evaluation(predicted_edoal)

    # ── Stage runners ──────────────────────────────────────────────────────────

    def _run_preprocessing(self):
        start = time.time()
        cfg = self.config.preprocessing
        self.preprocessing = Preprocessing(
            self.config.dataset_name,
            self.config.ontology_source_name,
            self.config.ontology_target_name,
            relations_to_remove=cfg.relations_to_remove,
        )
        source_modularizer = PPRModularizer() if cfg.modularizer_type == "ppr" else PageRankModularizer()
        source_modules, _ = source_modularizer.generate_modules(
            self.preprocessing.ontology_pair.ontology_source_nx_graph,
            max_length=cfg.max_length_pagerank,
            depth=cfg.depth,
            max_length_subgraph=cfg.max_length_subgraph,
        )
        target_modules, sample_target_subgraph = SampleModularizer().generate_modules(
            self.preprocessing.ontology_pair.ontology_target_nx_graph,
            max_length=cfg.max_length_target_sample,
            depth=cfg.depth,
            max_length_subgraph=cfg.max_length_subgraph,
        )
        mlflow.log_metric("preprocessing.time_sec", time.time() - start)
        mlflow.log_artifact(
            PROJECT_ROOT / "outputs/preprocessing/source_modules.json",
            artifact_path="preprocessing",
        )
        mlflow.log_artifact(
            PROJECT_ROOT / "outputs/preprocessing/target_modules.json",
            artifact_path="preprocessing",
        )
        return source_modules, target_modules, sample_target_subgraph

    def _run_verbalizer(self, modules, verbalizer_type, dataset_name, ontology_name):
        start = time.time()
        verbalizer = BuildVerbalizer.build(verbalizer_type, dataset_name, ontology_name)
        modules_triples = [verbalizer.verbalize(module) for module in modules]
        mlflow.log_metric(f"verbalizer_{verbalizer_type}.time_sec", time.time() - start)
        return [TextStringVerbalizer().verbalize(module) for module in modules_triples], verbalizer

    def _run_candidate_gen(self, source_modules, target_modules, ontology_target_path, sample_target_subgraph):
        start = time.time()
        cfg = self.config.candidate_generation
        candidates = CandidateGeneration(
            cfg.embedding_model_name,
            padding_side=cfg.padding_side,
            batch_size=cfg.batch_size,
            backend=cfg.backend,
            padding=cfg.padding,
            max_length=cfg.max_length,
        ).forward(
            source_modules,
            target_modules,
            sample_target_subgraph,
            ontology_target_path,
            max_similarities=cfg.max_similarities,
            relations_to_remove=cfg.relations_to_remove,
        )
        mlflow.log_metric("candidate_gen.time_sec", time.time() - start)
        mlflow.log_artifact(
            PROJECT_ROOT / "outputs/candidate_generation/candidates.json",
            artifact_path="candidate_generation",
        )
        mlflow.log_artifact(
            PROJECT_ROOT / "outputs/candidate_generation/entities_similarities.json",
            artifact_path="candidate_generation",
        )
        return candidates

    def _run_matching(self, candidates):
        start = time.time()
        cfg = self.config.matching
        llm_outputs = Matching(
            cfg.llm_model,
            max_model_len=cfg.max_model_len,
            max_num_batched_tokens=cfg.max_num_batched_tokens,
            K=cfg.k,
            seed=int(self.seed),
            verbalizer_type=self.config.verbalizer_type.matcher,
            backend=cfg.backend,
            n_gpu_layers=cfg.get("n_gpu_layers", -1),
        ).forward(candidates)
        mlflow.log_metric("matching.time_sec", time.time() - start)
        mlflow.log_artifact(
            PROJECT_ROOT / "outputs/matching/prompts.json", artifact_path="matching"
        )
        mlflow.log_artifact(
            PROJECT_ROOT / "outputs/matching/results.json", artifact_path="matching"
        )
        return llm_outputs

    def _run_postprocessing(self, outputs):
        start = time.time()
        onto_source = self.config.ontology_source_name
        onto_target = self.config.ontology_target_name
        self.final_result = Postprocessing(
            onto_source, onto_target, self.source_concept_dict, self.target_concept_dict
        ).forward(outputs)
        mlflow.log_metric("postprocessing.time_sec", time.time() - start)
        mlflow.log_artifact(
            PROJECT_ROOT / f"outputs/postprocessing/{onto_source}-{onto_target}.txt",
            artifact_path="postprocessing",
        )
        return self.final_result

    def _run_evaluation(self, predicted_edoal) -> None:
        start = time.time()
        cfg = self.config
        evaluation = Evaluation(
            cfg.dataset_name,
            cfg.ontology_source_name,
            cfg.ontology_target_name,
        )
        precision, recall, f1 = evaluation.forward(predicted_edoal, ignore_errors=True)
        mlflow.log_metric("evaluation.precision", precision)
        mlflow.log_metric("evaluation.recall", recall)
        mlflow.log_metric("evaluation.f1", f1)
        mlflow.log_metric("evaluation.time_sec", time.time() - start)
        self._metrics = {"precision": precision, "recall": recall, "f1": f1}


# ── Hydra entry point — single-pair runner ────────────────────────────────────

@hydra.main(config_path=".", config_name="config", version_base=None)
def main(cfg: DictConfig):
    mlflow.set_tracking_uri("sqlite:///mlflow.db")
    mlflow.set_experiment(f"om_pipeline_single_{cfg.dataset_name}")

    pair = f"{cfg.ontology_source_name}-{cfg.ontology_target_name}"
    seed = int(cfg.get("seeds", 42))
    now = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')

    run_name = f"om_{cfg.dataset_name}_{pair}_{now}"

    with mlflow.start_run(run_name=run_name):
        mlflow.set_tag("dataset", cfg.dataset_name)
        mlflow.set_tag("ontology_pair", pair)
        mlflow.set_tag("seed", seed)
        pipeline = OMPipeline(cfg)
        metrics = pipeline.run(seed)

    print(metrics)


if __name__ == "__main__":
    main()