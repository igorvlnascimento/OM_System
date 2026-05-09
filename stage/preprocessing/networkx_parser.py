from rdflib import Graph

from stage.preprocessing.ontology_parser import OntologyParser
from stage.preprocessing.rdflib_to_networkx import rdflib_to_networkx

@OntologyParser.register("networkx")
class NetworkxOntologyParser(OntologyParser):
    def parse(self, ontology_path=None, graph=None, relations_to_remove=[]):
        if graph is None:
            graph = Graph().parse(ontology_path)
        return rdflib_to_networkx(
            g=graph,
            relations_to_remove=relations_to_remove
        )
    