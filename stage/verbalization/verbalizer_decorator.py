from abc import ABC, abstractmethod

# Interface comum
class Verbalizer(ABC):      
    @abstractmethod
    def verbalize_triple(self, module: list) -> list:
        """Verbalize a list of (subject, relation, object) triples."""
        pass

    def verbalize(self, iri):
        pass
    
    def build_concept_dict(self, triples, verbalize_function):
        concept_dict = {}
        for triple in triples:
            for iri in triple:
                key = str(iri)
                if key not in concept_dict:
                    concept_dict[key] = verbalize_function(iri)
        return concept_dict
    
    def get_label_from_iri(self, iri):
        return iri.split("#")[-1] if "#" in iri else iri.split("/")[-1]

class VerbalizerDecorator(Verbalizer):
    def __init__(self, component: Verbalizer):
        self._component = component
