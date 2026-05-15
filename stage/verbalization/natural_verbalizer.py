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
        self.concept_dict = {}

    def _compute_label(self, iri):
        return self._apply_strategies(self._component.verbalize(iri))

    def _apply_strategies(self, text):
        for strategy in self.strategies:
            if strategy.matches(text):
                return strategy.verbalize(text)
        return text
