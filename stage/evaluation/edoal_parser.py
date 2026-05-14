from pathlib import Path


class EDOALParser:
    def __init__(self, root="references"):
        self.root = Path(root)

    def parse(self, dataset, ontology_source_name, ontology_target_name):
        filepath = self.root / dataset / f"{ontology_source_name}-{ontology_target_name}.edoal"
        with open(filepath, "r") as f:
            return f.read()