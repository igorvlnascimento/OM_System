from abc import ABC, abstractmethod
from pathlib import Path
import mlflow

from stage.preprocessing.ontology_pair import get_pair

CURRENT = Path(__file__).resolve()
PROJECT_ROOT = ""

for parent in CURRENT.parents:
    if (parent / "pyproject.toml").exists():
        PROJECT_ROOT = parent
        break

class PromptGenerator(ABC):
    def __init__(self, sample1=True, sample2=True, verbalizer_type="label") -> None:
        self.sample1 = sample1
        self.sample2 = sample2
        self.verbalizer_type = verbalizer_type
        self.source_prefix, self.target_prefix = get_pair().get_prefixes()
        get_pair().reset()
        

    @abstractmethod
    def generate_prompt(self, source_module, target_module):
        pass

    @mlflow.trace(name="prompt")
    def generate_instruction_prompt(self, source_module, target_module):
        sample_prompt = ''
        instruction = "Write a file in EDOAL format containing the complex alignment between the input ontologies <ontology1> and <ontology2>. " \
        "You don't need to explain yourself. Just give as response the resulting alignment file without saying anything else."

        if self.sample1 or self.sample2:
            sample_prompt = 'Based on the examples of the task of complex ontology alignment between the ontologies below with the results written in EDOAL format:'

        sample1_prompt, sample2_prompt = self.get_samples_prompt()


        return f'''
{sample_prompt}\n
{sample1_prompt}\n
{sample2_prompt}\n\n
{instruction}\n
Given the two ontologies below:\n
<ontology1>
{source_module}
</ontology1>
<ontology2>
{target_module}
</ontology2>
'''

    def get_samples_prompt(self):
        sample1_prompt = ''
        sample2_prompt = ''
        if self.sample1:
            with open(PROJECT_ROOT / f'samples/sample1_{self.verbalizer_type}.txt', 'r') as f:
                sample1_prompt = f.read()
        if self.sample2:
            with open(PROJECT_ROOT / f'samples/sample2_{self.verbalizer_type}.txt', 'r') as f:
                sample2_prompt = f.read()

        return sample1_prompt, sample2_prompt


