from stage.candidate_generation.candidate_generation import CandidateGeneration
from stage.evaluation.evaluation import Evaluation
from stage.matching.matching import Matching
from stage.postprocessing.postprocessing import Postprocessing
from stage.modularization.modularizer import PPRModularizer
from stage.preprocessing.preprocessing import Preprocessing


def test_evaluation():
    dataset, pair1, pair2 = "conference", "cmt", "conference"
    preprocessing = Preprocessing(dataset, pair1, pair2)
    source_modules, target_modules, sample_target_subgraph = preprocessing.forward()
    cand_generation = CandidateGeneration("sentence-transformers/all-MiniLM-L6-v2")
    candidates = cand_generation.forward(source_modules, 
                                     target_modules, 
                                     sample_target_subgraph,
                                     preprocessing.ontology_target_path)
    modules = Matching("HuggingFaceTB/SmolLM-135M-Instruct", max_model_len=2048).forward(candidates)
    llm_response = Postprocessing("cmt", "conference").forward(modules)
    evaluation = Evaluation(dataset, pair1, pair2)
    final_result = evaluation.forward(llm_response)
    assert final_result == (0, 0, 0)

def test_evaluation_with_ppr():
    dataset, pair1, pair2 = "conference", "cmt", "conference"
    preprocessing = Preprocessing(dataset, pair1, pair2)
    source_modules, target_modules, sample_target_subgraph = preprocessing.forward(modularizer=PPRModularizer())
    cand_generation = CandidateGeneration("sentence-transformers/all-MiniLM-L6-v2")
    candidates = cand_generation.forward(source_modules, 
                                     target_modules, 
                                     sample_target_subgraph,
                                     preprocessing.ontology_target_path)
    modules = Matching("HuggingFaceTB/SmolLM-135M-Instruct", max_model_len=2048).forward(candidates)
    llm_response = Postprocessing("cmt", "conference").forward(modules)
    evaluation = Evaluation(dataset, pair1, pair2)
    final_result = evaluation.forward(llm_response)
    assert final_result == (0, 0, 0)
    