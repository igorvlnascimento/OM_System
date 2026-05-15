from stage.matching.build_llm_model import BuildLLMModel
from stage.matching.llm_model_vllm import LLMModelVLLM
from stage.matching.prompt_generator_transformers import PromptGeneratorTransformers

def test_buid_model_vllm():
    llm, prompt = BuildLLMModel.build("HuggingFaceTB/SmolLM-135M")
    assert type(llm) == LLMModelVLLM
    assert type(prompt) == PromptGeneratorTransformers