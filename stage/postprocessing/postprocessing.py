import os
from pathlib import Path
import re
from bs4 import BeautifulSoup
from lxml import etree
from stage.postprocessing.answer_extractor import AnswerExtractor

from stage.postprocessing.xml_parser_refinement import XMLParserRefinement

CURRENT = Path(__file__).resolve()
PROJECT_ROOT = ""

for parent in CURRENT.parents:
    if (parent / "pyproject.toml").exists():
        PROJECT_ROOT = parent
        break

CACHE_DIR = str(PROJECT_ROOT / "tmp")

class Postprocessing:
    def __init__(self, ontology_source_name, ontology_target_name, source_concept_dict=None, target_concept_dict=None):
        self.ontology_source_name = ontology_source_name
        self.ontology_target_name = ontology_target_name
        self.source_concept_dict = source_concept_dict or {}
        self.target_concept_dict = target_concept_dict or {}

    def forward(self, llm_outputs):
        all_edoals_list = []
        for output in llm_outputs:
            try:
                BeautifulSoup(self.extract_answer(output), features='xml')
                all_edoals_list.append(self.extract_answer(output))
            except:
                pass
        edoal = BeautifulSoup(self.merge_edoals(all_edoals_list), features='xml').prettify()
        xml_parser = XMLParserRefinement(edoal)
        root = xml_parser.parse()
        xml_parser.refine(root, self.source_concept_dict, "source")
        xml_parser.refine(root, self.target_concept_dict, "target")
        final_edoal = etree.tostring(root, pretty_print=True, encoding="unicode")
        self.generate_edoal_file(final_edoal)

        return final_edoal
    
    def extract_answer(self, output):
        return AnswerExtractor.llm_response(output)
    
    def merge_edoals(self, outputs):
        repaired_edoals = []
        for output in outputs:

            if not output.startswith('<?xml version'):
                output = '''<?xml version='1.0' encoding='utf-8' standalone='no'?>
        <rdf:RDF xmlns='http://knowledgeweb.semanticweb.org/heterogeneity/alignment#'
            xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#'
            xmlns:xsd='http://www.w3.org/2001/XMLSchema#'
            xmlns:alext='http://exmo.inrialpes.fr/align/ext/1.0/'
            xmlns:align='http://knowledgeweb.semanticweb.org/heterogeneity/alignment#'
            xmlns:edoal='http://ns.inria.org/edoal/1.0/#'>\n''' + output

            output = re.sub(r'<Ontology rdf:about="([^"]+)" />',
                            r'<Ontology rdf:about="\1"><location>\1</location><formalism><Formalism align:name="owl" align:uri="http://www.w3.org/TR/owl-guide/"/></formalism></Ontology>',
                            output)
            if not self.is_valid_edoal(output) and self.can_repair(output):
                last_map_index = output.rfind('<map>')
                repaired_edoals.append(output[:last_map_index] + '\n\t</Alignment>\n</rdf:RDF>')
            else:
                repaired_edoals.append(output)

        final_edoal = None
        if len(repaired_edoals) > 1:
            final_edoal = ''
            first = repaired_edoals[0]
            final_edoal += first[:first.find('<map>')]
            for e in repaired_edoals[1:]:
                final_edoal += e[e.find('<map>'):e.rfind('</map>')] + '\n\t</map>'

            final_edoal += '\n\t</Alignment>\n</rdf:RDF>'

        elif len(repaired_edoals) == 1:
            final_edoal = repaired_edoals[0]

        return final_edoal
    
    def is_valid_edoal(self, edoal):
        return edoal.endswith('</rdf:RDF>')


    def can_repair(self, edoal):
        return edoal.rfind('<map>') > 0
    
    def generate_edoal_file(self, final_edoal):
        POSTPROCESSING_PATH = PROJECT_ROOT / "outputs/postprocessing"
        os.makedirs(POSTPROCESSING_PATH, exist_ok=True)
        with open(POSTPROCESSING_PATH / f'{self.ontology_source_name}-{self.ontology_target_name}.txt', 'w') as f:
            f.write(final_edoal)

    