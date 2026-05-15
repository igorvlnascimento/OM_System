from stage.preprocessing.networkx_parser import NetworkxOntologyParser
from stage.verbalization.verbalizer_decorator import Verbalizer


class BaseVerbalizer(Verbalizer):
    def __init__(self, ontology_path: str) -> None:
        nx_graph = NetworkxOntologyParser().parse(ontology_path=ontology_path)
        self.concept_dict = {}
        for u, v, data in nx_graph.edges(data=True):
            for iri in (u, data["relation"], v):
                self._ensure_label(iri)
