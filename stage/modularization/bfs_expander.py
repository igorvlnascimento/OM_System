from collections import deque
import random
from rdflib import OWL, RDF, XSD, BNode, Graph, Literal

import networkx as nx

class BFSExpander:
    @staticmethod
    def get_sample(G: nx.MultiDiGraph, size=3000):
        H = G.copy()
        nodes_length = len(H.nodes())
        k = min(size, nodes_length)
        sample_nodes = random.sample(list(H.nodes()), k)
        return list(G.subgraph(sample_nodes).copy())

    def bfs(self, nx_graph: nx.MultiGraph, 
                                      entities: list, 
                                      depth=1, 
                                      max_length=20):
        G = nx.MultiDiGraph()
        for entity in entities:
            H = nx_graph.subgraph(list(nx.ego_graph(nx_graph, n=entity, radius=depth, undirected=True))[:max_length]).copy()
            G = nx.compose(G, H)
        return G