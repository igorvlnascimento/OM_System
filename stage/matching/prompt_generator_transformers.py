from pathlib import Path
from transformers import AutoTokenizer

from stage.matching.prompt_generator import PromptGenerator

CURRENT = Path(__file__).resolve()
PROJECT_ROOT = ""

for parent in CURRENT.parents:
    if (parent / "pyproject.toml").exists():
        PROJECT_ROOT = parent
        break

class PromptGeneratorTransformers(PromptGenerator):
    def __init__(self, model_id, sample1=True, sample2=True, verbalizer_type="base", padding_side='left'):
        super().__init__(sample1=sample1, sample2=sample2, verbalizer_type=verbalizer_type)
        self.llm_tokenizer = AutoTokenizer.from_pretrained(model_id, padding_side=padding_side, trust_remote_code=True)
        self.llm_tokenizer.pad_token = self.llm_tokenizer.eos_token if self.llm_tokenizer.eos_token is not None else self.llm_tokenizer.pad_token


    def generate_prompt(self, source_module, target_module):
        chat =  [
            {'role': 'system', 'content': 'You are a Complex Ontology Matching expert.'},
            {'role': 'user', 'content': self.generate_instruction_prompt(source_module, target_module)},
        ]
        return self.llm_tokenizer.apply_chat_template(
            chat,
            tokenize=False,
            add_generation_prompt=True,
            enable_thinking=True
        )
