import os
from pathlib import Path
from stage.preprocessing.ontology_pair import init_ontology_pair

CURRENT = Path(__file__).resolve()
PROJECT_ROOT = ""

for parent in CURRENT.parents:
    if (parent / "pyproject.toml").exists():
        PROJECT_ROOT = parent
        break

class Preprocessing:
    def __init__(self,
                 dataset_name,
                 ontology_source_name,
                 ontology_target_name,
                 datasets_root='datasets',
                 relations_to_remove=[]):
        if os.path.isfile(PROJECT_ROOT / Path(datasets_root) / dataset_name / f"{ontology_source_name}.owl"):
            self.ontology_source_path = PROJECT_ROOT / Path(datasets_root) / dataset_name / f"{ontology_source_name}.owl"
        else:
            self.ontology_source_path = PROJECT_ROOT / Path(datasets_root) / dataset_name / f"{ontology_source_name}.rdf"
        if os.path.isfile(PROJECT_ROOT / Path(datasets_root) / dataset_name / f"{ontology_target_name}.owl"):
            self.ontology_target_path = PROJECT_ROOT / Path(datasets_root) / dataset_name / f"{ontology_target_name}.owl"
        else:
            self.ontology_target_path = PROJECT_ROOT / Path(datasets_root) / dataset_name / f"{ontology_target_name}.rdf"

        self.ontology_pair = init_ontology_pair(self.ontology_source_path, self.ontology_target_path, relations_to_remove=relations_to_remove)

        self.ontology_source_name = ontology_source_name
        self.ontology_target_name = ontology_target_name
