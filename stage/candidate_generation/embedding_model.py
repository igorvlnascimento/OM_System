from abc import ABC, abstractmethod
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CACHE_DIR = str(BASE_DIR / "tmp")

class EmbeddingModel(ABC):
    @abstractmethod
    def similarity(self, embeddings1, embedding2):
        pass

    @abstractmethod
    def encode(self, input_texts, truncation=True):
        pass

    @abstractmethod
    def clean_memory(self):
        pass


        