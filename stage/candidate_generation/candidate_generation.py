import json
import os
from pathlib import Path

from stage.candidate_generation.build_embedding_model import BuildEmbeddingModel
from rdflib import Graph
from stage.preprocessing.networkx_parser import NetworkxOntologyParser
from stage.modularization.bfs_expander import BFSExpander

CURRENT = Path(__file__).resolve()
PROJECT_ROOT = ""

for parent in CURRENT.parents:
    if (parent / "pyproject.toml").exists():
        PROJECT_ROOT = parent
        break

CACHE_DIR = PROJECT_ROOT / "tmp"

class CandidateGeneration:
    def __init__(self,
                 embedding_model_name,
                 cache_dir=CACHE_DIR,
                 batch_size=2,
                 padding_side='left',
                 backend="vllm",
                 padding=True,
                 max_length=4096):
        self.embedding_model = BuildEmbeddingModel.build(
            embedding_model_name=embedding_model_name,
            cache_dir=cache_dir,
            batch_size=batch_size,
            padding_side=padding_side,
            backend=backend,
            padding=padding,
            max_length=max_length,
        )

    def forward(self,
                source_data,
                target_data,
                target_subgraph,
                target_ontology_path,
                max_similarities=5,
                max_length=20,
                relations_to_remove=["disjointWith"]):
        
        source_embeddings = self.embedding_model.encode(source_data)
        target_embeddings = self.embedding_model.encode(target_data)

        assert len(source_embeddings) == 15

        similarities = self.embedding_model.similarity(source_embeddings, target_embeddings)

        self.embedding_model.clean_memory()

        entities = [sorted(enumerate(l), key=lambda x: x[1], reverse=True) for l in similarities.tolist()]
        filtered_entities = [[x for x in l][:max_similarities] for l in entities]

        candidates = {}
        for i, x in enumerate(filtered_entities):
            candidates[(i, source_data[i])] = [(target_subgraph[q], w) for q, w in x]

        candidates_filtered = {}
        for i, x in enumerate(filtered_entities):
            candidates_filtered[source_data[i]] = [(target_subgraph[q], w) for q, w in x]

        assert all([candidate for candidate in candidates_filtered if len(candidate) > 0])

        self.generate_json_modules(candidates_filtered, "candidates")

        entities_similarities = {}
        for i, x in enumerate(entities):
            entities_similarities[source_data[i]] = [(target_data[q], w) for q, w in x]

        self.generate_json_modules(entities_similarities, "entities_similarities")

        assert len(candidates) == 15

        modules = []
        target_graph = Graph().parse(target_ontology_path)
        target_nx_graph = NetworkxOntologyParser().parse(graph=target_graph, relations_to_remove=relations_to_remove)
        for (_, source_module), target_list in candidates.items():
            new_target_subgraph = BFSExpander().bfs(
                target_nx_graph, 
                [target for target, _ in target_list],
                max_length=max_length,
            )
            target_module = [(u, data["relation"], v) for u, v, data in new_target_subgraph.edges(data=True)]
            modules.append((source_module, target_module))
        assert len(modules) == 15
        self.generate_json_modules(modules, "candidates")
        return modules

    def generate_json_modules(self, modules, filename):
        CAND_GEN_PATH = PROJECT_ROOT / 'outputs/candidate_generation'
        os.makedirs(CAND_GEN_PATH, exist_ok=True)

        with open(CAND_GEN_PATH / f'{filename}.json', 'w') as f:
            json.dump(modules, f, indent=4, ensure_ascii=False)


        

        


