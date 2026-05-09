from pathlib import Path
from typing import Tuple
from stage.matching.llm_model import LLMModel
from stage.matching.llm_model_llamacpp import LLMModelLlamaCPP
from stage.matching.llm_model_ollama import LLMModelOllama
from stage.matching.llm_model_vllm import LLMModelVLLM
from stage.matching.prompt_generator import PromptGenerator
from stage.matching.prompt_generator_ollama import PromptGeneratorOllama
from stage.matching.prompt_generator_transformers import PromptGeneratorTransformers

CURRENT = Path(__file__).resolve()
PROJECT_ROOT = ""

for parent in CURRENT.parents:
    if (parent / "pyproject.toml").exists():
        PROJECT_ROOT = parent
        break

CACHE_DIR = str(PROJECT_ROOT / "tmp")

class BuildLLMModel():
    @staticmethod
    def build(llm_model_name,
              dtype="float16",
              max_model_len=None,
              max_num_batched_tokens=None,
              K=1,
              seed=42,
              padding_side='left',
              verbalizer_type="label",
              backend="vllm",
              n_gpu_layers=-1) -> Tuple[LLMModel, PromptGenerator]:
        if backend == "ollama":
            llm_model = LLMModelOllama(llm_model_name,
                                       max_model_length=max_model_len,
                                       seed=seed)
            prompt_template = PromptGeneratorOllama(verbalizer_type=verbalizer_type)
            return llm_model, prompt_template
        elif backend == "llamacpp":
            llm_model = LLMModelLlamaCPP(
                model_name=llm_model_name,
                n_ctx=max_model_len or 4096,
                seed=seed,
                n_gpu_layers=n_gpu_layers,
            )
            prompt_template = PromptGeneratorOllama(verbalizer_type=verbalizer_type)
            return llm_model, prompt_template
        elif backend == "vllm":
           llm_model = LLMModelVLLM(
                model_name=llm_model_name,
                dtype=dtype,
                max_model_length=max_model_len,
                padding_side=padding_side,
                max_num_batched_tokens=max_num_batched_tokens,
                K=K,
                seed=seed
            )
           prompt_template = PromptGeneratorTransformers(llm_model_name, verbalizer_type=verbalizer_type, padding_side=padding_side)
           return llm_model, prompt_template
        else:
            llm_model = LLMModelVLLM(
                model_name=llm_model_name,
                dtype=dtype,
                max_model_length=max_model_len,
                padding_side=padding_side,
                max_num_batched_tokens=max_num_batched_tokens,
                K=K,
                seed=seed
            )
            prompt_template = PromptGeneratorTransformers(llm_model_name, verbalizer_type=verbalizer_type, padding_side=padding_side)
            return llm_model, prompt_template