import json
import os
from abc import ABC, abstractmethod
from pathlib import Path

import networkx as nx

from stage.modularization.pagerank import PageRankBase, PersonalisedPageRank
from stage.modularization.bfs_expander import BFSExpander

CURRENT = Path(__file__).resolve()
PROJECT_ROOT = ""

for parent in CURRENT.parents:
    if (parent / "pyproject.toml").exists():
        PROJECT_ROOT = parent
        break


class Modularizer(ABC):
    @abstractmethod
    def generate_modules(self,
                         nx_graph: nx.MultiDiGraph,
                         max_length: int = 15,
                         depth: int = 1,
                         max_length_subgraph: int = 20,
                         **kwargs) -> tuple:
        """
        Generate modules from an ontology graph.

        Returns:
            modules: list of modules, each a list of (subject, relation, object) triples
            centers: list of center node groups used to generate the modules
        """
        pass

    def generate_json_modules(self, module_name: str, modules: dict):
        preprocessing_path = PROJECT_ROOT / "outputs/preprocessing"
        os.makedirs(preprocessing_path, exist_ok=True)
        with open(preprocessing_path / f"{module_name}.json", "w") as f:
            json.dump(modules, f, indent=4, ensure_ascii=False)


class PageRankModularizer(Modularizer):
    def __init__(self):
        self.page_rank = PageRankBase()
        self.bfs_expander = BFSExpander()

    def generate_modules(self,
                         nx_graph: nx.MultiDiGraph,
                         max_length: int = 15,
                         depth: int = 1,
                         max_length_subgraph: int = 20,
                         damping_factor: float = 0.8,
                         num_iterations: int = 100,
                         **kwargs) -> tuple:
        centers = self.page_rank.execute(nx_graph, damping_factor, num_iterations)[:max_length]
        subgraphs = [
            self.bfs_expander.bfs(nx_graph, entities, depth=depth, max_length=max_length_subgraph)
            for entities in centers
        ]
        modules = [[(u, data["relation"], v) for u, v, data in sg.edges(data=True)] for sg in subgraphs]
        self.generate_json_modules("source_modules", {centers[i][0]: modules[i] for i in range(len(centers))})
        return modules, centers


class PPRModularizer(Modularizer):
    def __init__(self):
        self.page_rank = PageRankBase()
        self.bfs_expander = BFSExpander()

    def generate_modules(self,
                         nx_graph: nx.MultiDiGraph,
                         max_length: int = 15,
                         depth: int = 1,
                         max_length_subgraph: int = 20,
                         damping_factor: float = 0.8,
                         num_iterations: int = 100,
                         max_ppr_ranks: int = 2,
                         **kwargs) -> tuple:
        ppr = PersonalisedPageRank(self.page_rank)
        centers = ppr.execute(nx_graph, damping_factor, num_iterations, max_ppr_ranks)[:max_length]
        subgraphs = [
            self.bfs_expander.bfs(nx_graph, entities, depth=depth, max_length=max_length_subgraph)
            for entities in centers
        ]
        modules = [[(u, data["relation"], v) for u, v, data in sg.edges(data=True)] for sg in subgraphs]
        self.generate_json_modules("source_modules", {centers[i][0]: modules[i] for i in range(len(centers))})
        return modules, centers


class SampleModularizer(Modularizer):
    def __init__(self):
        self.subgraph_generator = BFSExpander()

    def generate_modules(self,
                         nx_graph: nx.MultiDiGraph,
                         max_length: int = 3000,
                         depth: int = 1,
                         max_length_subgraph: int = 20,
                         **kwargs) -> tuple:
        sample = BFSExpander.get_sample(nx_graph, size=max_length)
        subgraphs = [
            self.subgraph_generator.bfs(nx_graph, [entity], depth=depth, max_length=max_length_subgraph)
            for entity in sample
        ]
        modules = [[(u, data["relation"], v) for u, v, data in sg.edges(data=True)] for sg in subgraphs]
        self.generate_json_modules("target_modules", {sample[i]: modules[i] for i in range(len(sample))})
        return modules, sample