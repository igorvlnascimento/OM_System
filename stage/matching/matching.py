import json
import os
from pathlib import Path

from stage.matching.build_llm_model import BuildLLMModel

CURRENT = Path(__file__).resolve()
PROJECT_ROOT = ""

for parent in CURRENT.parents:
    if (parent / "pyproject.toml").exists():
        PROJECT_ROOT = parent
        break

class Matching:
    def __init__(self,
                 llm_model,
                 dtype="float16",
                 max_model_len=None,
                 max_num_batched_tokens=None,
                 K=1,
                 seed=42,
                 padding_side='left',
                 verbalizer_type="label",
                 backend="vllm",
                 n_gpu_layers=-1):
        self.llm_model, self.prompt_template = BuildLLMModel.build(llm_model,
                                                                   dtype=dtype,
                                                                   max_model_len=max_model_len,
                                                                   max_num_batched_tokens=max_num_batched_tokens,
                                                                   K=K,
                                                                   seed=seed,
                                                                   padding_side=padding_side,
                                                                   verbalizer_type=verbalizer_type,
                                                                   backend=backend,
                                                                   n_gpu_layers=n_gpu_layers)

    def forward(self, modules):
        prompts = [self.prompt_template.generate_prompt(source_module, target_module) for source_module, target_module in zip(modules[0], modules[1])]
        llm_outputs = self.llm_model.generate(prompts)
        self.generate_prompts_json(prompts)
        self.generate_outputs_json(llm_outputs)
        self.llm_model.clean_memory()
        return llm_outputs

    def generate_outputs_json(self, outputs):
        outputs = [out.split("\n") for out in outputs]
        MATCH_PATH = PROJECT_ROOT / "outputs/matching"
        os.makedirs(MATCH_PATH, exist_ok=True)
        with open(MATCH_PATH / "results.json", "w") as f:
            json.dump(outputs, f, indent=4, ensure_ascii=False)

    def generate_prompts_json(self, prompts):
        MATCH_PATH = PROJECT_ROOT / "outputs/matching"
        os.makedirs(MATCH_PATH, exist_ok=True)
        with open(MATCH_PATH / "prompts.json", "w") as f:
            json.dump(prompts, f, indent=4, ensure_ascii=False)