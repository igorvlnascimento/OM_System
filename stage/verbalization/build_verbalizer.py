import os
from pathlib import Path
from stage.verbalization.base_verbalizer import BaseVerbalizer
from stage.verbalization.label_verbalizer import LabelVerbalizer
from stage.verbalization.natural_verbalizer import DefaultStrategy, EquivalentClassStrategy, InverseOfStrategy, NaturalVerbalizer, SubClassOfStrategy, SubPropertyOfStrategy, TypeStrategy
from stage.verbalization.verbalizer_decorator import Verbalizer

CURRENT = Path(__file__).resolve()
PROJECT_ROOT = ""

for parent in CURRENT.parents:
    if (parent / "pyproject.toml").exists():
        PROJECT_ROOT = parent
        break

STRATEGIES = [
    SubClassOfStrategy(),
    SubPropertyOfStrategy(),
    TypeStrategy(),
    EquivalentClassStrategy(),
    InverseOfStrategy(),
    DefaultStrategy(),
]

class BuildVerbalizer():
    @staticmethod
    def build(verbalizer, dataset_name, ontology_name, datasets_root='datasets') -> Verbalizer:
        if verbalizer == "base":
            if os.path.isfile(PROJECT_ROOT / Path(datasets_root) / dataset_name / f"{ontology_name}.owl"):
                return BaseVerbalizer(PROJECT_ROOT / Path(datasets_root) / dataset_name / f"{ontology_name}.owl")
            else:
                return BaseVerbalizer(PROJECT_ROOT / Path(datasets_root) / dataset_name / f"{ontology_name}.rdf")
        elif verbalizer == "label":
            if os.path.isfile(PROJECT_ROOT / Path(datasets_root) / dataset_name / f"{ontology_name}.owl"):
                return LabelVerbalizer(PROJECT_ROOT / Path(datasets_root) / dataset_name / f"{ontology_name}.owl")
            else:
                return LabelVerbalizer(PROJECT_ROOT / Path(datasets_root) / dataset_name / f"{ontology_name}.rdf")
        elif verbalizer == "natural":
            if os.path.isfile(PROJECT_ROOT / Path(datasets_root) / dataset_name / f"{ontology_name}.owl"):
                verbalizer = LabelVerbalizer(PROJECT_ROOT / Path(datasets_root) / dataset_name / f"{ontology_name}.owl")
                return NaturalVerbalizer(verbalizer, STRATEGIES)
            else:
                verbalizer = LabelVerbalizer(PROJECT_ROOT / Path(datasets_root) / dataset_name / f"{ontology_name}.rdf")
                return NaturalVerbalizer(verbalizer, STRATEGIES)
        else:
            if os.path.isfile(PROJECT_ROOT / Path(datasets_root) / dataset_name / f"{ontology_name}.owl"):
                return BaseVerbalizer(PROJECT_ROOT / Path(datasets_root) / dataset_name / f"{ontology_name}.owl")
            else:
                return BaseVerbalizer(PROJECT_ROOT / Path(datasets_root) / dataset_name / f"{ontology_name}.rdf")