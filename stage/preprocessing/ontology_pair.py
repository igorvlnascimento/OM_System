from rdflib import Graph

from stage.preprocessing.networkx_parser import NetworkxOntologyParser


class OntologyPair:
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, ontology_source_path, ontology_target_path, relations_to_remove=[]):
        self.ontology_source_graph = Graph().parse(ontology_source_path)
        self.ontology_target_graph = Graph().parse(ontology_target_path)
        self.ontology_source_nx_graph = NetworkxOntologyParser().parse(ontology_source_path, relations_to_remove=relations_to_remove)
        self.ontology_target_nx_graph = NetworkxOntologyParser().parse(ontology_target_path, relations_to_remove=relations_to_remove)

    @classmethod
    def reset(cls):
        global _pair
        _pair = None
        cls._instance = None

    def get_ontology_source(self):
        return self.ontology_source_graph

    def get_ontology_target(self):
        return self.ontology_target_graph

    def get_ontology_pair(self):
        return self.ontology_source_nx_graph, self.ontology_target_nx_graph
    
    def get_prefixes(self):
        source_node = list(self.ontology_source_nx_graph.nodes())[0]
        target_node = list(self.ontology_target_nx_graph.nodes())[0]
        return self.get_prefix(source_node), self.get_prefix(target_node)

    def get_prefix(self, node):
        return str(node).split("#")[0] + "#" if "#" in str(node) else str(node).split("/")[0] + "/"

_pair = None

def init_ontology_pair(ontology_source_path, ontology_target_path, relations_to_remove=[]):
    global _pair
    if _pair is None:
        _pair = OntologyPair(ontology_source_path, ontology_target_path, relations_to_remove=relations_to_remove)
    return _pair

def get_pair():
    return _pair