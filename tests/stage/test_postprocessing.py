from stage.candidate_generation.candidate_generation import CandidateGeneration
from stage.matching.matching import Matching
from stage.postprocessing.postprocessing import Postprocessing
from stage.preprocessing.ontology_pair import OntologyPair
from stage.preprocessing.preprocessing import Preprocessing
from stage.verbalization.build_verbalizer import BuildVerbalizer
from stage.verbalization.text_string_verbalizer import TextStringVerbalizer


def test_postprocessing():
    OntologyPair.reset()
    preprocessing = Preprocessing("conference", "cmt", "conference", relations_to_remove=["disjointWith"])
    source_modules, target_modules, sample_target_subgraph = preprocessing.forward()
    source_verbalizer = BuildVerbalizer.build("natural", "conference", "cmt")
    target_verbalizer = BuildVerbalizer.build("natural", "conference", "conference")
    source_modules = [TextStringVerbalizer().verbalize(source_verbalizer.verbalize(source_module)) for source_module in source_modules]
    target_modules = [TextStringVerbalizer().verbalize(target_verbalizer.verbalize(target_module)) for target_module in target_modules]
    cand_generation = CandidateGeneration("sentence-transformers/all-MiniLM-L6-v2")
    candidates = cand_generation.forward(source_modules,
                                     target_modules,
                                     sample_target_subgraph,
                                     preprocessing.ontology_target_path)
    target_modules = [TextStringVerbalizer().verbalize(target_verbalizer.verbalize(target_module)) for _, target_module in candidates]
    llm_responses = Matching("smollm:135m", backend="ollama").forward(candidates)
    result = Postprocessing("cmt", "conference").forward(llm_responses)
    for source in source_modules:
        print("source:", source)
        if source:
            for triple in source.split("\n"):
                assert len(triple.split()) == 3
    for target in target_modules:
        print("target:", target)
        if target:
            for triple in target.split("\n"):
                assert len(triple.split()) == 3
    assert type(result) == str or result == None
    