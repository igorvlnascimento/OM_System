from rdflib import Graph
from stage.preprocessing.ontology_pair import OntologyPair

import networkx as nx


def test_ontology_pair():
    source = "datasets/conference/cmt.owl"
    target = "datasets/conference/conference.owl"

    pair = OntologyPair(source, target)
    source_nx_graph, target_nx_graph = pair.get_ontology_pair()
    assert type(pair.get_ontology_source()) == Graph
    assert type(pair.get_ontology_target()) == Graph
    assert type(source_nx_graph) == nx.MultiDiGraph
    assert type(target_nx_graph) == nx.MultiDiGraph
    assert len(source_nx_graph.nodes()) > 0
    assert len(target_nx_graph.nodes()) > 0