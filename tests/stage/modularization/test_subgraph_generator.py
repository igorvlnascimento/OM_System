import pytest
from rdflib import OWL, RDFS, Graph, URIRef

from stage.preprocessing.networkx_parser import NetworkxOntologyParser
from stage.modularization.bfs_expander import BFSExpander

@pytest.fixture(scope="module")
def source_nx_graph():
    graph = Graph().parse("datasets/conference/cmt.owl")
    return NetworkxOntologyParser().parse(graph=graph)


def test_subgraph_generator_target():
    graph = Graph().parse("datasets/conference/cmt.owl")
    target_nx_graph = NetworkxOntologyParser().parse(graph=graph)
    subgraph_target = BFSExpander.generate_sample(target_nx_graph)
    assert 0 < len(subgraph_target) <= 3000

# def test_subgraph_generator_source_old_approach():
#     graph = Graph().parse("datasets/conference/cmt.owl")
#     subgraph_source = BFSExpander.generate_subgraph_by_entities_old_approach(graph, [URIRef("http://cmt#Conference")])
#     all_nodes_subgraph = set(subgraph_source.subjects()) | set(subgraph_source.predicates()) | set(subgraph_source.objects())
#     print(all_nodes_subgraph)
#     assert len(all_nodes_subgraph) > 20

def test_subgraph_generator_source_only_one_co_author(source_nx_graph):
    subgraph_source = BFSExpander().generate(source_nx_graph, [URIRef("http://cmt#Co-author")])
    all_nodes_subgraph = subgraph_source.nodes()
    all_edges_subgraph = subgraph_source.edges()
    assert len(all_nodes_subgraph) == 4
    assert len(all_edges_subgraph) == 3

def test_subgraph_generator_source_only_one_user(source_nx_graph):
    subgraph_source = BFSExpander().generate(source_nx_graph, [URIRef("http://cmt#User")])
    all_nodes_subgraph = subgraph_source.nodes()
    all_edges_subgraph = subgraph_source.edges()
    assert len(all_nodes_subgraph) == 5
    assert len(all_edges_subgraph) == 4

def test_subgraph_generator_not_repeated_nodes_user(source_nx_graph):
    subgraph_source = BFSExpander().generate(source_nx_graph, [URIRef("http://cmt#User")])
    all_nodes_subgraph = list(subgraph_source.nodes())
    assert all([node1 != node2 for i, node1 in enumerate(all_nodes_subgraph) for node2 in all_nodes_subgraph[i+1:]])

def test_subgraph_generator_source_more_than_one(source_nx_graph):
    subgraph_source = BFSExpander().generate(source_nx_graph, [URIRef("http://cmt#Co-author"), URIRef("http://cmt#User")])
    all_nodes_subgraph = subgraph_source.nodes()
    all_edges_subgraph = subgraph_source.edges()
    assert len(all_nodes_subgraph) == 8
    assert len(all_edges_subgraph) == 7

def test_subgraph_generator_not_repeated_nodes_co_author(source_nx_graph):
    subgraph_source = BFSExpander().generate(source_nx_graph, [URIRef("http://cmt#Co-author"), URIRef("http://cmt#User")])
    all_nodes_subgraph = list(subgraph_source.nodes())
    assert all([node1 != node2 for i, node1 in enumerate(all_nodes_subgraph) for node2 in all_nodes_subgraph[i+1:]])