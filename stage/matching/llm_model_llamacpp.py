from typing import Dict, List

from stage.model_registry import ModelRegistryFactory
from stage.matching.llm_model import LLMModel


class LLMModelLlamaCPP(LLMModel):
    def __init__(
        self,
        model_name: str,
        n_ctx: int = 4096,
        max_output_tokens: int = 512,
        n_gpu_layers: int = -1,
        seed: int = 42,
    ):
        self.model_name = model_name
        self.max_output_tokens = max_output_tokens
        self.registry = ModelRegistryFactory.get("llamacpp")
        self.registry.load(
            model_name,
            n_ctx=n_ctx,
            n_gpu_layers=n_gpu_layers,
            seed=seed,
        )

    def generate(self, prompts: List[Dict[str, str]]) -> List[str]:
        return self.registry.generate(
            self.model_name,
            prompts,
            max_tokens=self.max_output_tokens,
        )

    def clean_memory(self) -> None:
        self.registry.unload(self.model_name)
