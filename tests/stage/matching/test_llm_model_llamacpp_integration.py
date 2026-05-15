"""Integration test for LLMModelLlamaCPP using the real LFM2.5-1.2B GGUF model.

Run with:
    uv run pytest tests/matching/test_llm_model_llamacpp_integration.py -v -s
"""
import pytest
from pathlib import Path

MODEL_PATH = "models/1.2B/LFM2.5-1.2B-Instruct-Q4_K_M.gguf"

pytestmark = pytest.mark.skipif(
    not Path(MODEL_PATH).exists(),
    reason=f"Model file not found: {MODEL_PATH}",
)


@pytest.fixture(scope="module")
def llm_model():
    from pipeline.matching.llm_model_llamacpp import LLMModelLlamaCPP

    model = LLMModelLlamaCPP(
        model_name=MODEL_PATH,
        n_ctx=2048,
        max_output_tokens=256,
        n_gpu_layers=0,
        seed=42,
    )
    yield model
    model.clean_memory()


def test_generate_returns_nonempty_string(llm_model):
    prompts = [[{"role": "user", "content": "Say hello in one sentence."}]]
    results = llm_model.generate(prompts)

    assert isinstance(results, list)
    assert len(results) == 1
    assert isinstance(results[0], str)
    assert len(results[0].strip()) > 0


def test_generate_multiple_prompts(llm_model):
    prompts = [
        [{"role": "user", "content": "What is 2 + 2? Answer with just the number."}],
        [{"role": "user", "content": "What is the capital of France? Answer in one word."}],
    ]
    results = llm_model.generate(prompts)

    assert len(results) == 2
    assert all(isinstance(r, str) and len(r.strip()) > 0 for r in results)


def test_generate_with_system_prompt(llm_model):
    prompts = [[
        {"role": "system", "content": "You are a helpful assistant. Be concise."},
        {"role": "user",   "content": "Name one planet in our solar system."},
    ]]
    results = llm_model.generate(prompts)

    assert isinstance(results[0], str)
    assert len(results[0].strip()) > 0


def test_generate_is_deterministic(llm_model):
    """Same seed should produce the same output for the same prompt."""
    from pipeline.matching.llm_model_llamacpp import LLMModelLlamaCPP

    prompt = [[{"role": "user", "content": "Name a color."}]]

    model_a = LLMModelLlamaCPP(MODEL_PATH, n_ctx=512, max_output_tokens=32, n_gpu_layers=0, seed=7)
    model_b = LLMModelLlamaCPP(MODEL_PATH, n_ctx=512, max_output_tokens=32, n_gpu_layers=0, seed=7)

    result_a = model_a.generate(prompt)
    result_b = model_b.generate(prompt)

    model_a.clean_memory()
    model_b.clean_memory()

    assert result_a == result_b
