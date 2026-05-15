from unittest.mock import MagicMock, patch, call

import pytest

from stage.matching.llm_model_llamacpp import LLMModelLlamaCPP
from stage.model_registry import LlamaCPPModelRegistry


# ─── LLMModelLlamaCPP ─────────────────────────────────────────────────────────

class TestLLMModelLlamaCPP:
    def test_load_called_on_init(self):
        with patch("pipeline.matching.llm_model_llamacpp.ModelRegistryFactory") as MockFactory:
            mock_registry = MagicMock()
            MockFactory.get.return_value = mock_registry

            LLMModelLlamaCPP("path/to/model.gguf", n_ctx=2048, n_gpu_layers=0, seed=1)

            MockFactory.get.assert_called_once_with("llamacpp")
            mock_registry.load.assert_called_once_with(
                "path/to/model.gguf",
                n_ctx=2048,
                n_gpu_layers=0,
                seed=1,
            )

    def test_load_default_n_gpu_layers(self):
        with patch("pipeline.matching.llm_model_llamacpp.ModelRegistryFactory") as MockFactory:
            mock_registry = MagicMock()
            MockFactory.get.return_value = mock_registry

            LLMModelLlamaCPP("path/to/model.gguf")

            _, call_kwargs = mock_registry.load.call_args
            assert call_kwargs["n_gpu_layers"] == -1

    def test_load_default_n_ctx(self):
        with patch("pipeline.matching.llm_model_llamacpp.ModelRegistryFactory") as MockFactory:
            mock_registry = MagicMock()
            MockFactory.get.return_value = mock_registry

            LLMModelLlamaCPP("path/to/model.gguf")

            _, call_kwargs = mock_registry.load.call_args
            assert call_kwargs["n_ctx"] == 4096

    def test_generate_delegates_to_registry(self):
        with patch("pipeline.matching.llm_model_llamacpp.ModelRegistryFactory") as MockFactory:
            mock_registry = MagicMock()
            mock_registry.generate.return_value = ["answer"]
            MockFactory.get.return_value = mock_registry

            model = LLMModelLlamaCPP("path/to/model.gguf", max_output_tokens=256)
            prompts = [[{"role": "user", "content": "hi"}]]
            result = model.generate(prompts)

            mock_registry.generate.assert_called_once_with(
                "path/to/model.gguf", prompts, max_tokens=256
            )
            assert result == ["answer"]

    def test_generate_default_max_tokens(self):
        with patch("pipeline.matching.llm_model_llamacpp.ModelRegistryFactory") as MockFactory:
            mock_registry = MagicMock()
            mock_registry.generate.return_value = ["answer"]
            MockFactory.get.return_value = mock_registry

            model = LLMModelLlamaCPP("path/to/model.gguf")
            model.generate([[{"role": "user", "content": "hi"}]])

            _, call_kwargs = mock_registry.generate.call_args
            assert call_kwargs["max_tokens"] == 512

    def test_generate_returns_list(self):
        with patch("pipeline.matching.llm_model_llamacpp.ModelRegistryFactory") as MockFactory:
            mock_registry = MagicMock()
            mock_registry.generate.return_value = ["r1", "r2"]
            MockFactory.get.return_value = mock_registry

            model = LLMModelLlamaCPP("path/to/model.gguf")
            result = model.generate([
                [{"role": "user", "content": "a"}],
                [{"role": "user", "content": "b"}],
            ])

            assert isinstance(result, list)
            assert result == ["r1", "r2"]

    def test_generate_passes_all_prompts(self):
        with patch("pipeline.matching.llm_model_llamacpp.ModelRegistryFactory") as MockFactory:
            mock_registry = MagicMock()
            mock_registry.generate.return_value = ["x", "y", "z"]
            MockFactory.get.return_value = mock_registry

            prompts = [
                [{"role": "user", "content": "q1"}],
                [{"role": "user", "content": "q2"}],
                [{"role": "user", "content": "q3"}],
            ]
            model = LLMModelLlamaCPP("path/to/model.gguf")
            result = model.generate(prompts)

            args, _ = mock_registry.generate.call_args
            assert args[1] is prompts
            assert len(result) == 3

    def test_clean_memory_unloads(self):
        with patch("pipeline.matching.llm_model_llamacpp.ModelRegistryFactory") as MockFactory:
            mock_registry = MagicMock()
            MockFactory.get.return_value = mock_registry

            model = LLMModelLlamaCPP("path/to/model.gguf")
            model.clean_memory()

            mock_registry.unload.assert_called_once_with("path/to/model.gguf")


# ─── LlamaCPPModelRegistry._truncate_messages ─────────────────────────────────

def _make_mock_llm(n_ctx: int, tokens_per_char: int = 1):
    """Return a mock llm whose tokenize/detokenize/n_ctx behave predictably.

    Each character in the text maps to `tokens_per_char` integer tokens.
    """
    llm = MagicMock()
    llm.n_ctx.return_value = n_ctx

    def tokenize(text, **kwargs):
        # Return one token-id per character (as ints) for determinism.
        return list(range(len(text) * tokens_per_char))

    def detokenize(tokens):
        # Reverse: each token maps back to one character ('a').
        n_chars = len(tokens) // tokens_per_char
        return b"a" * n_chars

    llm.tokenize.side_effect = tokenize
    llm.detokenize.side_effect = detokenize
    return llm


class TestLlamaCPPTruncateMessages:
    def test_no_truncation_when_fits(self):
        # 10-char messages → 10 tokens total; budget = 100 - 10 - 64 = 26 → fits
        llm = _make_mock_llm(n_ctx=100)
        messages = [
            {"role": "system", "content": "hello"},
            {"role": "user",   "content": "world"},
        ]
        result = LlamaCPPModelRegistry._truncate_messages(llm, messages, max_tokens=10)
        assert result == messages

    def test_truncates_last_user_message(self):
        # n_ctx=80, max_tokens=10, overhead=64 → budget=6
        # system: 3 tokens, user: 100 tokens → total=103 > 6 → truncate user
        llm = _make_mock_llm(n_ctx=80)
        messages = [
            {"role": "system", "content": "abc"},        # 3 tokens
            {"role": "user",   "content": "x" * 100},   # 100 tokens
        ]
        result = LlamaCPPModelRegistry._truncate_messages(llm, messages, max_tokens=10)

        assert result[0]["content"] == "abc"   # system unchanged
        assert len(result[1]["content"]) < 100  # user was truncated

    def test_system_message_unchanged_during_truncation(self):
        llm = _make_mock_llm(n_ctx=80)
        messages = [
            {"role": "system", "content": "sys_prompt"},
            {"role": "user",   "content": "u" * 200},
        ]
        result = LlamaCPPModelRegistry._truncate_messages(llm, messages, max_tokens=10)

        assert result[0] == {"role": "system", "content": "sys_prompt"}

    def test_does_not_mutate_original_messages(self):
        llm = _make_mock_llm(n_ctx=80)
        original_content = "u" * 200
        messages = [
            {"role": "system", "content": "sys"},
            {"role": "user",   "content": original_content},
        ]
        LlamaCPPModelRegistry._truncate_messages(llm, messages, max_tokens=10)

        assert messages[1]["content"] == original_content

    def test_truncated_user_content_at_least_one_token(self):
        # Extremely tight budget: even 1 token barely fits.
        llm = _make_mock_llm(n_ctx=66)   # budget = 66 - 10 - 64 = -8 → forces max(1, ...)
        messages = [
            {"role": "user", "content": "hello world this is a long message"},
        ]
        result = LlamaCPPModelRegistry._truncate_messages(llm, messages, max_tokens=10)
        # Should not raise and user content must be non-empty (at least 1 token kept).
        assert len(result[0]["content"]) >= 1

    def test_returns_copy_not_same_objects(self):
        llm = _make_mock_llm(n_ctx=80)
        messages = [
            {"role": "system", "content": "s"},
            {"role": "user",   "content": "u" * 200},
        ]
        result = LlamaCPPModelRegistry._truncate_messages(llm, messages, max_tokens=10)
        assert result is not messages
        assert result[0] is not messages[0]

    def test_custom_overhead(self):
        # With a larger overhead the budget shrinks further → more truncation.
        llm = _make_mock_llm(n_ctx=200)
        long_user = "u" * 150
        messages = [{"role": "user", "content": long_user}]

        result_small_overhead = LlamaCPPModelRegistry._truncate_messages(
            llm, messages, max_tokens=10, overhead=10
        )
        result_large_overhead = LlamaCPPModelRegistry._truncate_messages(
            llm, messages, max_tokens=10, overhead=100
        )
        # Larger overhead → smaller budget → more aggressive truncation.
        assert len(result_large_overhead[0]["content"]) <= len(result_small_overhead[0]["content"])


# ─── LlamaCPPModelRegistry.generate ───────────────────────────────────────────

class TestLlamaCPPRegistryGenerate:
    def _make_registry(self):
        registry = LlamaCPPModelRegistry()
        registry._models = {}
        return registry

    def _make_entry(self, n_ctx: int = 4096):
        llm = MagicMock()
        llm.n_ctx.return_value = n_ctx
        llm.tokenize.side_effect = lambda text, **kw: list(range(len(text)))
        llm.detokenize.side_effect = lambda t: b"a" * len(t)

        fake_response = {
            "choices": [{"message": {"content": "generated text"}}]
        }
        llm.create_chat_completion.return_value = fake_response
        return {"llm": llm, "seed": 42}

    def test_generate_calls_create_chat_completion(self):
        registry = self._make_registry()
        entry = self._make_entry()
        registry._models["my_model"] = entry

        prompts = [[{"role": "user", "content": "hi"}]]
        registry.generate("my_model", prompts, max_tokens=64)

        assert entry["llm"].create_chat_completion.call_count == 1

    def test_generate_extracts_content_from_response(self):
        registry = self._make_registry()
        entry = self._make_entry()
        registry._models["my_model"] = entry

        results = registry.generate("my_model", [[{"role": "user", "content": "q"}]], max_tokens=64)

        assert results == ["generated text"]

    def test_generate_called_once_per_prompt(self):
        registry = self._make_registry()
        entry = self._make_entry()
        registry._models["my_model"] = entry

        prompts = [
            [{"role": "user", "content": "q1"}],
            [{"role": "user", "content": "q2"}],
            [{"role": "user", "content": "q3"}],
        ]
        registry.generate("my_model", prompts, max_tokens=64)

        assert entry["llm"].create_chat_completion.call_count == 3

    def test_generate_passes_max_tokens(self):
        registry = self._make_registry()
        entry = self._make_entry()
        registry._models["my_model"] = entry

        registry.generate("my_model", [[{"role": "user", "content": "q"}]], max_tokens=128)

        _, kwargs = entry["llm"].create_chat_completion.call_args
        assert kwargs["max_tokens"] == 128

    def test_generate_passes_seed(self):
        registry = self._make_registry()
        entry = self._make_entry()
        entry["seed"] = 99
        registry._models["my_model"] = entry

        registry.generate("my_model", [[{"role": "user", "content": "q"}]], max_tokens=64)

        _, kwargs = entry["llm"].create_chat_completion.call_args
        assert kwargs["seed"] == 99

    def test_generate_raises_for_unknown_model(self):
        registry = self._make_registry()
        with pytest.raises(RuntimeError, match="not loaded"):
            registry.generate("nonexistent", [[{"role": "user", "content": "q"}]])
