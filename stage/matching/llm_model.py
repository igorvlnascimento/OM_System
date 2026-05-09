from abc import ABC, abstractmethod

from typing import List

class LLMModel(ABC):
    @abstractmethod
    def generate(self, input_texts) -> List[str]:
        pass

    @abstractmethod
    def clean_memory(self) -> None:
        pass