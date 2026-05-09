import numpy as np

from stage.model_registry import ModelRegistryFactory
from stage.candidate_generation.embedding_model import EmbeddingModel


class EmbeddingModelLlamaCPP(EmbeddingModel):
    def __init__(
        self,
        model_name: str,
        n_ctx: int = 512,
        seed: int = 42,
    ) -> None:
        self.model_name = model_name
        self.registry = ModelRegistryFactory.get("llamacpp")
        self.registry.load(model_name, n_ctx=n_ctx, seed=seed, embedding=True)

    def similarity(self, embeddings1, embeddings2):
        a = np.array(embeddings1)
        b = np.array(embeddings2)
        return np.dot(a, b.T) / (np.linalg.norm(a) * np.linalg.norm(b))

    def encode(self, input_texts, truncation=True):
        return self.registry.encode(self.model_name, input_texts, truncation=truncation)

    def clean_memory(self) -> None:
        self.registry.unload(self.model_name)
