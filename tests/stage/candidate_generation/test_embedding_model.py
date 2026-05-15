from unittest.mock import MagicMock, patch

import numpy as np
import torch

from stage.candidate_generation.embedding_model_transformers import EmbeddingModelTransformers
from stage.candidate_generation.embedding_model_ollama import EmbeddingModelOllama


# ─── EmbeddingModelTransformers ───────────────────────────────────────────────

class TestEmbeddingModelTransformers:
    def _make_registry(self):
        registry = MagicMock()
        tokenizer = MagicMock()
        tokenizer.padding_side = "left"
        registry.get_tokenizer.return_value = tokenizer
        return registry

    def test_load_called_on_init(self):
        with patch("stage.candidate_generation.embedding_model_transformers.ModelRegistryFactory") as MockFactory:
            mock_registry = self._make_registry()
            MockFactory.get.return_value = mock_registry

            EmbeddingModelTransformers("some/model", use_cuda=False)

            MockFactory.get.assert_called_once_with("transformers")
            mock_registry.load.assert_called_once_with("some/model", device="cpu")

    def test_load_uses_cuda_when_available(self):
        with patch("stage.candidate_generation.embedding_model_transformers.ModelRegistryFactory") as MockFactory:
            mock_registry = self._make_registry()
            MockFactory.get.return_value = mock_registry

            EmbeddingModelTransformers("some/model", use_cuda=True)

            mock_registry.load.assert_called_once_with("some/model", device="cuda")

    def test_encode_delegates_to_registry(self):
        with patch("stage.candidate_generation.embedding_model_transformers.ModelRegistryFactory") as MockFactory:
            mock_registry = self._make_registry()
            MockFactory.get.return_value = mock_registry

            n, dim = 2, 8
            # tokenizer returns CPU tensors
            mock_registry.get_tokenizer.return_value.return_value = {
                "input_ids": torch.zeros(n, 4, dtype=torch.long),
                "attention_mask": torch.ones(n, 4, dtype=torch.long),
            }
            # run_from_input_ids returns a mock with last_hidden_state
            hidden = torch.randn(1, 4, dim)
            mock_output = MagicMock()
            mock_output.last_hidden_state = hidden
            mock_registry.run_from_input_ids.return_value = mock_output

            model = EmbeddingModelTransformers("some/model", use_cuda=False, batch_size=2)
            result = model.encode(["hello", "world"])

            assert mock_registry.run_from_input_ids.called
            assert result.shape[1] == dim

    def test_clean_memory_unloads(self):
        with patch("stage.candidate_generation.embedding_model_transformers.ModelRegistryFactory") as MockFactory:
            mock_registry = self._make_registry()
            MockFactory.get.return_value = mock_registry

            model = EmbeddingModelTransformers("some/model", use_cuda=False)
            model.clean_memory()

            mock_registry.unload.assert_called_once_with("some/model")

    def test_similarity(self):
        with patch("stage.candidate_generation.embedding_model_transformers.ModelRegistryFactory") as MockFactory:
            mock_registry = self._make_registry()
            MockFactory.get.return_value = mock_registry

            model = EmbeddingModelTransformers("some/model", use_cuda=False)
            a = torch.tensor([[1.0, 0.0]])
            b = torch.tensor([[1.0, 0.0], [0.0, 1.0]])
            sim = model.similarity(a, b)
            assert sim.shape == (1, 2)


# ─── EmbeddingModelOllama ─────────────────────────────────────────────────────

class TestEmbeddingModelOllama:
    def test_load_called_on_init(self):
        with patch("stage.candidate_generation.embedding_model_ollama.ModelRegistryFactory") as MockFactory:
            mock_registry = MagicMock()
            MockFactory.get.return_value = mock_registry

            EmbeddingModelOllama("nomic-embed-text", max_length=1024, seed=7)

            MockFactory.get.assert_called_once_with("ollama")
            mock_registry.load.assert_called_once_with(
                "nomic-embed-text", max_model_length=1024, seed=7
            )

    def test_encode_delegates_to_registry(self):
        with patch("stage.candidate_generation.embedding_model_ollama.ModelRegistryFactory") as MockFactory:
            mock_registry = MagicMock()
            mock_registry.encode.return_value = [[0.1, 0.2], [0.3, 0.4]]
            MockFactory.get.return_value = mock_registry

            model = EmbeddingModelOllama("nomic-embed-text")
            result = model.encode(["hello", "world"], truncation=False)

            mock_registry.encode.assert_called_once_with(
                "nomic-embed-text", ["hello", "world"], truncation=False
            )
            assert result == [[0.1, 0.2], [0.3, 0.4]]

    def test_clean_memory_unloads(self):
        with patch("stage.candidate_generation.embedding_model_ollama.ModelRegistryFactory") as MockFactory:
            mock_registry = MagicMock()
            MockFactory.get.return_value = mock_registry

            model = EmbeddingModelOllama("nomic-embed-text")
            model.clean_memory()

            mock_registry.unload.assert_called_once_with("nomic-embed-text")

    def test_similarity_cosine(self):
        with patch("stage.candidate_generation.embedding_model_ollama.ModelRegistryFactory") as MockFactory:
            MockFactory.get.return_value = MagicMock()

            model = EmbeddingModelOllama("nomic-embed-text")
            a = np.array([[1.0, 0.0]])
            b = np.array([[1.0, 0.0]])
            sim = model.similarity(a, b)
            assert abs(sim - 1.0) < 1e-6
