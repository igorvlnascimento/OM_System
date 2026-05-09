from typing import List

from stage.verbalization.verbalizer_decorator import Verbalizer, VerbalizerDecorator


class TextStringVerbalizer(VerbalizerDecorator):
    def __init__(self, component: Verbalizer=None):
        self._component = component

    def verbalize_triple(self, module: list) -> list:
        return module

    def verbalize(self, triples) -> List[tuple]:
        if triples:
            return "\n".join([" ".join(triple) for triple in triples])
        return ""