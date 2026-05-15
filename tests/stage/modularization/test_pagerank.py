import pytest
from rdflib import Graph, URIRef
from stage.modularization.pagerank import PageRankBase, PersonalisedPageRank
from stage.preprocessing.rdflib_to_networkx import rdflib_to_networkx

@pytest.fixture(scope="module")
def graph():
    return Graph(). parse("../datasets/conference/cmt.owl")

def flatten_ranks(ranks):
    return [rank[0] for rank in ranks]

def test_pagerank(graph):
    pagerank = PageRankBase()
    nx_graph = rdflib_to_networkx(graph)
    baseline_sorted = [r for r in pagerank.execute(nx_graph)]
    assert all([len(base) == 1 for base in baseline_sorted])

def test_pagerank_has_main_entity(graph):
    pagerank = PageRankBase()
    nx_graph = rdflib_to_networkx(graph)
    baseline_sorted = [r for r in pagerank.execute(nx_graph)]
    assert URIRef("http://cmt#Conference") in flatten_ranks(baseline_sorted)[:3]

def test_personalised_pagerank(graph):
    pagerank = PageRankBase()
    nx_graph = rdflib_to_networkx(graph)
    ppr_sorted = [r for r in PersonalisedPageRank(pagerank).execute(nx_graph, max_ppr_ranks=2)]
    assert all(len(ppr) == 2 for ppr in ppr_sorted)

def test_personalised_pagerank_different_ranks(graph):
    pagerank = PageRankBase()
    nx_graph = rdflib_to_networkx(graph)
    ppr_sorted = [r for r in PersonalisedPageRank(pagerank).execute(nx_graph, max_ppr_ranks=2)]
    print(ppr_sorted)
    assert all(ppr[0] != ppr[1] for ppr in ppr_sorted)