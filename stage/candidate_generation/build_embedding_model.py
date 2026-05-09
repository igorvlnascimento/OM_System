from pathlib import Path
from stage.candidate_generation.embedding_model import EmbeddingModel
from stage.candidate_generation.embedding_model_llamacpp import EmbeddingModelLlamaCPP
from stage.candidate_generation.embedding_model_ollama import EmbeddingModelOllama
from stage.candidate_generation.embedding_model_transformers import EmbeddingModelTransformers

CURRENT = Path(__file__).resolve()
PROJECT_ROOT = ""

for parent in CURRENT.parents:
    if (parent / "pyproject.toml").exists():
        PROJECT_ROOT = parent
        break

class BuildEmbeddingModel():
    @staticmethod
    def build(embedding_model_name,
              cache_dir,
              batch_size=2,
              padding_side='left',
              backend="vllm",
              padding=True,
              max_length=4096) -> EmbeddingModel:
        if backend == "ollama":
            return EmbeddingModelOllama(
                embedding_model_name
            )
        elif backend == "llamacpp":
            return EmbeddingModelLlamaCPP(
                embedding_model_name,
                n_ctx=max_length,
            )
        elif backend == "vllm":
            return EmbeddingModelTransformers(
                embedding_model_name,
                cache_dir=cache_dir,
                padding_side=padding_side,
                padding=padding,
                batch_size=batch_size
            )
        else:
            return EmbeddingModelTransformers(
                embedding_model_name,
                cache_dir=cache_dir,
                padding_side=padding_side,
                padding=padding,
                batch_size=batch_size
            )
        