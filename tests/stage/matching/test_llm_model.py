from unittest.mock import MagicMock, patch

from stage.matching.llm_model_vllm import LLMModelVLLM
from stage.matching.llm_model_ollama import LLMModelOllama


# ─── LLMModelVLLM ─────────────────────────────────────────────────────────────

class TestLLMModelVLLM:
    def test_load_called_on_init(self):
        with patch("pipeline.matching.llm_model_vllm.ModelRegistryFactory") as MockFactory:
            mock_registry = MagicMock()
            MockFactory.get.return_value = mock_registry

            LLMModelVLLM("HuggingFaceTB/SmolLM-135M", max_model_length=2048, K=1, seed=0)

            MockFactory.get.assert_called_once_with("vllm")
            mock_registry.load.assert_called_once_with(
                "HuggingFaceTB/SmolLM-135M",
                dtype="float16",
                max_model_len=2048,
                max_num_seqs=2,
                max_num_batched_tokens=None,
                padding_side="left",
                K=1,
                seed=0,
            )

    def test_generate_delegates_to_registry(self):
        with patch("pipeline.matching.llm_model_vllm.ModelRegistryFactory") as MockFactory:
            mock_registry = MagicMock()
            mock_registry.generate.return_value = ["out1", "out2"]
            MockFactory.get.return_value = mock_registry

            model = LLMModelVLLM("some/model")
            result = model.generate(["prompt1", "prompt2"])

            mock_registry.generate.assert_called_once_with("some/model", ["prompt1", "prompt2"])
            assert result == ["out1", "out2"]

    def test_generate_returns_list(self):
        with patch("pipeline.matching.llm_model_vllm.ModelRegistryFactory") as MockFactory:
            mock_registry = MagicMock()
            mock_registry.generate.return_value = ["response"]
            MockFactory.get.return_value = mock_registry

            model = LLMModelVLLM("some/model")
            result = model.generate(["hello"])

            assert isinstance(result, list)

    def test_clean_memory_unloads(self):
        with patch("pipeline.matching.llm_model_vllm.ModelRegistryFactory") as MockFactory:
            mock_registry = MagicMock()
            MockFactory.get.return_value = mock_registry

            model = LLMModelVLLM("some/model")
            model.clean_memory()

            mock_registry.unload.assert_called_once_with("some/model")


# ─── LLMModelOllama ───────────────────────────────────────────────────────────

class TestLLMModelOllama:
    def test_load_called_on_init(self):
        with patch("pipeline.matching.llm_model_ollama.ModelRegistryFactory") as MockFactory:
            mock_registry = MagicMock()
            MockFactory.get.return_value = mock_registry

            LLMModelOllama("llama3", max_model_length=4096, seed=99)

            MockFactory.get.assert_called_once_with("ollama")
            mock_registry.load.assert_called_once_with(
                "llama3", max_model_length=4096, seed=99
            )

    def test_generate_delegates_to_registry(self):
        with patch("pipeline.matching.llm_model_ollama.ModelRegistryFactory") as MockFactory:
            mock_registry = MagicMock()
            mock_registry.generate.return_value = ["reply"]
            MockFactory.get.return_value = mock_registry

            model = LLMModelOllama("llama3")
            prompts = [[{"role": "user", "content": "hello"}]]
            result = model.generate(prompts)

            mock_registry.generate.assert_called_once_with("llama3", prompts)
            assert result == ["reply"]

    def test_clean_memory_unloads(self):
        with patch("pipeline.matching.llm_model_ollama.ModelRegistryFactory") as MockFactory:
            mock_registry = MagicMock()
            MockFactory.get.return_value = mock_registry

            model = LLMModelOllama("llama3")
            model.clean_memory()

            mock_registry.unload.assert_called_once_with("llama3")
