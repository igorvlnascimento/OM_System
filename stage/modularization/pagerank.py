from abc import ABC, abstractmethod
from rdflib import OWL, XSD

import networkx as nx

import operator

class PageRank(ABC):
    @abstractmethod
    def execute(self, graph):
        pass

class PageRankBase(PageRank):
    def execute(self, G: nx.MultiDiGraph, damping_factor: float=0.8, num_iterations=100):
        H = G.copy()
        H = self.remove_nodes(H)
        page_ranks = self.page_rank(H, damping_factor=damping_factor, num_iterations=num_iterations)
        return self.get_nodes(self.sort(page_ranks))
    
    def remove_nodes(self, G: nx.MultiDiGraph):
        nodes_to_remove = [
            OWL.Class,
            OWL.ObjectProperty,
            OWL.DatatypeProperty,
            OWL.Thing,
            XSD.string,
            XSD.anyURI,
            XSD.date,
            XSD.time,
            XSD.dateTime
        ]
        G.remove_nodes_from(nodes_to_remove)
        return G
    
    def page_rank(self, G: nx.MultiDiGraph, start_node=None, damping_factor: float=0.8, num_iterations=100):
        if start_node:
            return nx.pagerank(G, 
                            alpha=damping_factor, 
                            max_iter=num_iterations,
                            personalization={start_node: 1})
        else:
            return nx.pagerank(G, 
                            alpha=damping_factor, 
                            max_iter=num_iterations,
                            personalization=None)
        
    def sort(self, entities):
        return sorted(entities.items(), key=operator.itemgetter(1), reverse=True)
    
    def get_nodes(self, ranks):
        return [[node] for node, _ in ranks]
 
class PageRankDecorator(PageRank):
    def __init__(self, component: PageRank):
        self._component = component
    
class PersonalisedPageRank(PageRankDecorator):
    def __init__(self, component):
        super().__init__(component)

    def execute(self, G: nx.MultiDiGraph, damping_factor: float=0.8, num_iterations:int = 100, max_ppr_ranks=2):
        centers = self._component.execute(G, damping_factor, num_iterations)
        new_centers = centers.copy()
        H = G.copy()
        H = self._component.remove_nodes(H)
        for i, node in enumerate(centers):
            start_node = node[0]
            if start_node:
                if start_node in H:
                    scores = self._component.page_rank(H, start_node=start_node, damping_factor=damping_factor, num_iterations=num_iterations)
                    sorted_entities = self._component.sort(scores)[:max_ppr_ranks]
                    #print("start_node:", start_node)
                    #print("sorted_entities:", sorted_entities)
                    new_centers[i] = new_centers[i] + ([sorted_entities[0][0]] if sorted_entities[0][0] != new_centers[i][0] else [sorted_entities[-1][0]])
                else:
                    print(f"Error: The class '{start_node}' was found in the ontology, but not in the graph")
                    return
            else:
                return
        return new_centers