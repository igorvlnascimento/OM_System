from abc import ABC, abstractmethod

from stage.verbalization.verbalizer_decorator import Verbalizer, VerbalizerDecorator

class VerbalizationStrategy(ABC):
    @abstractmethod
    def matches(self, text) -> bool:
        ...

    @abstractmethod
    def verbalize(self, text) -> str:
        ...
    
    def separate_words(self, text):
        if text:
            new_text = text[0].lower()
            for i, c in enumerate(text[1:]):
                if self.is_upper_case_letter(c, text[i]):
                    new_text += f'_{c}'
                elif self.is_space(c):
                   new_text += '_'
                else:
                    new_text += c
            return new_text.lower()
        return text
    
    def is_upper_case_letter(self, char, previous_char):
        return char.isupper() and previous_char.isalpha() and previous_char.islower()
    
    def is_underline(self, char):
        return char == "_"
    
    def is_space(self, char):
        return char == " "
    
class SubClassOfStrategy(VerbalizationStrategy):
    def matches(self, text) -> bool:
        return "subClassOf" == text

    def verbalize(self, text) -> str:
        return "is_a"
    
class SubPropertyOfStrategy(VerbalizationStrategy):
    def matches(self, text) -> bool:
        return "subPropertyOf" == text

    def verbalize(self, text) -> str:
        return "is_subproperty_of"
    
class TypeStrategy(VerbalizationStrategy):
    def matches(self, text) -> bool:
        return "type" == text

    def verbalize(self, text) -> str:
        return "is_type_of"

class EquivalentClassStrategy(VerbalizationStrategy):
    def matches(self, text) -> bool:
        return "equivalentClass" == text

    def verbalize(self, text) -> str:
        return "is_equivalent_to"
    
class InverseOfStrategy(VerbalizationStrategy):
    def matches(self, text) -> bool:
        return "inverseOf" == text

    def verbalize(self, text) -> str:
        return "is_inverse_of"
    
class DefaultStrategy(VerbalizationStrategy):
    def __init__(self):
        super().__init__()

    def matches(self, text):
        return True
    
    def verbalize(self, text) -> str:
        return self.separate_words(text)

class NaturalVerbalizer(VerbalizerDecorator):
    def __init__(self, component: Verbalizer, strategies: list[VerbalizationStrategy]):
        self._component = component
        self.strategies = strategies
        self.concept_dict = self.build_concept_dict([])

    def build_concept_dict(self, iris):
        concept_dict = self._component.concept_dict
        for verb in concept_dict.keys():
            for strategy in self.strategies:
                if strategy.matches(concept_dict[verb]):
                    new_verb = strategy.verbalize(concept_dict[verb])
                    concept_dict[verb] = new_verb
                    break
        return concept_dict
    
    def verbalize_triple(self, triple) -> tuple:
        triple = self._component.verbalize_triple(triple)
        new_triple = []
        for t in triple:
            for strategy in self.strategies:
                if strategy.matches(t):
                    t = strategy.verbalize(t)
                    new_triple.append(t)
                    break
        return tuple(new_triple)
    
    def verbalize(self, iri):
        key = str(iri)
        if key in self.concept_dict:
            return self.concept_dict[key]
        return self.set_strategies(self.get_label_from_iri(key))
    
    def set_strategies(self, label):
        new_label = label
        for strategy in self.strategies:
            if strategy.matches(new_label):
                new_label = strategy.verbalize(new_label)
        return new_label
