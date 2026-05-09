import xml
from stage.evaluation.complex_evaluate import evaluate_edoal_string
from stage.evaluation.edoal_parser import EDOALParser


class Evaluation:
    def __init__(self,
                 dataset_name,
                 ontology_source_name, 
                 ontology_target_name, 
                 weight=0.5, 
                 similarity_function=None):
        self.ontology_source_name = ontology_source_name
        self.ontology_target_name = ontology_target_name
        self.weight = weight
        self.similarity_function = similarity_function
        self.reference = EDOALParser().parse(dataset_name, ontology_source_name, ontology_target_name)


    def forward(self, llm_response, ignore_errors=False):
        try:
            return evaluate_edoal_string(llm_response, self.reference, ignore_errors=ignore_errors)
        except xml.etree.ElementTree.ParseError:
            return 0, 0, 0