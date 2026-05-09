from pathlib import Path
from typing import Dict, List
from stage.matching.prompt_generator import PromptGenerator

CURRENT = Path(__file__).resolve()
PROJECT_ROOT = ""

for parent in CURRENT.parents:
    if (parent / "pyproject.toml").exists():
        PROJECT_ROOT = parent
        break

class PromptGeneratorOllama(PromptGenerator):
    def __init__(self, sample1=True, sample2=True, verbalizer_type="label") -> None:
        super().__init__(sample1=sample1, sample2=sample2, verbalizer_type=verbalizer_type)
        
    def generate_prompt(self, source_module, target_module) -> List[Dict[str, str]]:
        chat =  [
            {'role': 'system', 'content': 'You are a Complex Ontology Matching expert.'},
            {'role': 'user', 'content': self.generate_instruction_prompt(source_module, target_module)},
        ]
        return chat