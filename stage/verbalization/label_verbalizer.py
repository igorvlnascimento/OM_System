from rdflib import Graph, RDFS, SKOS, URIRef

from stage.preprocessing.networkx_parser import NetworkxOntologyParser
from stage.verbalization.verbalizer_decorator import VerbalizerDecorator


class LabelVerbalizer(VerbalizerDecorator):
    def __init__(self, ontology_path: str):
        self._rdf_graph = Graph().parse(str(ontology_path))
        nx_graph = NetworkxOntologyParser().parse(graph=self._rdf_graph)
        self.concept_dict = {}
        for u, v, data in nx_graph.edges(data=True):
            for iri in (u, data["relation"], v):
                self._ensure_label(iri)

    def _compute_label(self, iri):
        node = iri if isinstance(iri, URIRef) else URIRef(str(iri))
        for predicate in (RDFS.label, SKOS.prefLabel):
            candidates = [
                str(lbl)
                for lbl in self._rdf_graph.objects(node, predicate)
                if " " not in str(lbl)
            ]
            if candidates:
                return candidates[-1]
        return self.get_label_from_iri(str(iri))
