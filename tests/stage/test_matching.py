import random

from stage.candidate_generation.candidate_generation import CandidateGeneration
from stage.matching.matching import Matching
from stage.preprocessing.preprocessing import Preprocessing


def test_matching():
    random.seed(42)
    dataset, pair1, pair2 = "conference", "cmt", "conference"
    preprocessing = Preprocessing(dataset, pair1, pair2)
    source_modules, target_modules, sample_target_subgraph = preprocessing.forward()
    cand_generation = CandidateGeneration("sentence-transformers/all-MiniLM-L6-v2")
    candidates = cand_generation.forward(source_modules, 
                                     target_modules, 
                                     sample_target_subgraph,
                                     preprocessing.ontology_target_path)
    llm_response = Matching("HuggingFaceTB/SmolLM-135M-Instruct").forward(
        candidates
    )
    assert isinstance(llm_response, list)
    assert len(llm_response) > 0