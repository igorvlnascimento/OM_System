from typing import List

from stage.model_registry import ModelRegistryFactory
from stage.matching.llm_model import LLMModel


class LLMModelVLLM(LLMModel):
    def __init__(
        self,
        model_name: str,
        cache_dir=None,
        dtype: str = "float16",
        max_model_length: int | None = None,
        padding_side: str = "left",
        max_num_batched_tokens: int | None = None,
        max_num_seqs: int = 2,
        K: int = 10,
        seed: int = 42,
    ):
        self.model_name = model_name
        self.registry = ModelRegistryFactory.get("vllm")
        self.registry.load(
            model_name,
            dtype=dtype,
            max_model_len=max_model_length,
            max_num_seqs=max_num_seqs,
            max_num_batched_tokens=max_num_batched_tokens,
            padding_side=padding_side,
            K=K,
            seed=seed,
        )

    def generate(self, input_texts: List[str]) -> List[str]:
        return self.registry.generate(self.model_name, input_texts)

    def clean_memory(self) -> None:
        self.registry.unload(self.model_name)
