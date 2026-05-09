from typing import Dict, List

from stage.model_registry import ModelRegistryFactory
from stage.matching.llm_model import LLMModel


class LLMModelOllama(LLMModel):
    def __init__(
        self,
        model_name: str,
        max_model_length: int | None = None,
        seed: int = 42,
    ):
        self.model_name = model_name
        self.registry = ModelRegistryFactory.get("ollama")
        self.registry.load(model_name, max_model_length=max_model_length, seed=seed)

    def generate(self, input_texts: List[Dict[str, str]]) -> List[str]:
        return self.registry.generate(self.model_name, input_texts)

    def clean_memory(self) -> None:
        self.registry.unload(self.model_name)
