from stage.preprocessing.networkx_parser import NetworkxOntologyParser
from stage.verbalization.verbalizer_decorator import Verbalizer

class BaseVerbalizer(Verbalizer):
    def __init__(self, ontology_path: str) -> None:
        nx_graph = NetworkxOntologyParser().parse(ontology_path=ontology_path)
        triples = [(u, data["relation"], v) for u, v, data in nx_graph.edges(data=True)]
        self.concept_dict = self.build_concept_dict(triples, self.verbalize)

    def verbalize_triple(self, module):
        return [
          tuple(self.verbalize(iri) if iri is not None else '' for iri in triple)
          for triple in module
        ]
    
    def verbalize(self, iri):
        return str(iri)