import random
import numpy as np
from stage.candidate_generation.candidate_generation import CandidateGeneration
from stage.preprocessing.ontology_pair import OntologyPair
from stage.modularization.modularizer import PPRModularizer
from stage.preprocessing.preprocessing import Preprocessing
from stage.verbalization.build_verbalizer import BuildVerbalizer
from stage.verbalization.text_string_verbalizer import TextStringVerbalizer


def test_candidate_generation():
    OntologyPair.reset()
    preprocessing = Preprocessing("conference", "cmt", "conference", relations_to_remove=["disjointWith"])
    preprocessing2 = Preprocessing("conference", "cmt", "conference", relations_to_remove=["disjointWith"])
    random.seed(42)
    source_modules, target_modules, sample_target_subgraph = preprocessing.forward()
    random.seed(42)
    source_modules2, target_modules2, sample_target_subgraph2 = preprocessing2.forward()
    verbalizer = BuildVerbalizer.build("label", "conference", "cmt")
    source_modules = [TextStringVerbalizer().verbalize(verbalizer.verbalize(source_module)) for source_module in source_modules]
    source_modules2 = [TextStringVerbalizer().verbalize(verbalizer.verbalize(source_module)) for source_module in source_modules2]
    cand_generation = CandidateGeneration("embeddinggemma", backend="ollama")
    cand_generation2 = CandidateGeneration("embeddinggemma", backend="ollama")
    np.random.seed(42)
    result = cand_generation.forward(source_modules,
                                     target_modules,
                                     sample_target_subgraph,
                                     preprocessing.ontology_target_path)
    np.random.seed(42)
    new_result = cand_generation2.forward(source_modules2,
                                     target_modules2,
                                     sample_target_subgraph2,
                                     preprocessing2.ontology_target_path)
    for i, res in enumerate(result):
        assert res[0] == new_result[i][0]
        assert res[1] == new_result[i][1]
    assert result == new_result
    assert type(result) == list
    assert len(result) > 0
    assert type(result[0]) == tuple
    assert any([len(result[i]) > 0 for i in range(len(result))])

def test_candidate_generation_with_ppr():
    OntologyPair.reset()
    preprocessing = Preprocessing("conference", "cmt", "conference", relations_to_remove=["disjointWith"])
    preprocessing2 = Preprocessing("conference", "cmt", "conference", relations_to_remove=["disjointWith"])
    random.seed(42)
    source_modules, target_modules, sample_target_subgraph = preprocessing.forward(modularizer=PPRModularizer())
    random.seed(42)
    source_modules2, target_modules2, sample_target_subgraph2 = preprocessing2.forward(modularizer=PPRModularizer())
    verbalizer = BuildVerbalizer.build("label", "conference", "cmt")
    source_modules = [TextStringVerbalizer().verbalize(verbalizer.verbalize(source_module)) for source_module in source_modules]
    source_modules2 = [TextStringVerbalizer().verbalize(verbalizer.verbalize(source_module)) for source_module in source_modules2]
    cand_generation = CandidateGeneration("embeddinggemma", backend="ollama")
    cand_generation2 = CandidateGeneration("embeddinggemma", backend="ollama")
    np.random.seed(42)
    result = cand_generation.forward(source_modules,
                                     target_modules,
                                     sample_target_subgraph,
                                     preprocessing.ontology_target_path)
    np.random.seed(42)
    new_result = cand_generation2.forward(source_modules2,
                                     target_modules2,
                                     sample_target_subgraph2,
                                     preprocessing2.ontology_target_path)
    for i, res in enumerate(result):
        assert res[0] == new_result[i][0]
        assert res[1] == new_result[i][1]
    assert result == new_result
    assert type(result) == list
    assert len(result) > 0
    assert any([len(result[i]) > 0 for i in range(len(result))])

def test_candidate_generation_with_ppr_label():
    OntologyPair.reset()
    preprocessing = Preprocessing("conference", "cmt", "conference", relations_to_remove=["disjointWith"])
    preprocessing2 = Preprocessing("conference", "cmt", "conference", relations_to_remove=["disjointWith"])
    random.seed(42)
    source_modules, target_modules, sample_target_subgraph = preprocessing.forward(modularizer=PPRModularizer())
    random.seed(42)
    source_modules2, target_modules2, sample_target_subgraph2 = preprocessing2.forward(modularizer=PPRModularizer())
    verbalizer = BuildVerbalizer.build("label", "conference", "cmt")
    source_modules = [TextStringVerbalizer().verbalize(verbalizer.verbalize(source_module)) for source_module in source_modules]
    source_modules2 = [TextStringVerbalizer().verbalize(verbalizer.verbalize(source_module)) for source_module in source_modules2]
    cand_generation = CandidateGeneration("embeddinggemma", backend="ollama")
    cand_generation2 = CandidateGeneration("embeddinggemma", backend="ollama")
    np.random.seed(42)
    result = cand_generation.forward(source_modules,
                                     target_modules,
                                     sample_target_subgraph,
                                     preprocessing.ontology_target_path)
    np.random.seed(42)
    new_result = cand_generation2.forward(source_modules2,
                                     target_modules2,
                                     sample_target_subgraph2,
                                     preprocessing2.ontology_target_path)
    for i, res in enumerate(result):
        assert res[0] == new_result[i][0]
        assert res[1] == new_result[i][1]
    assert result == new_result
    assert type(result) == list
    assert len(result) > 0
    assert any([len(result[i]) > 0 for i in range(len(result))])


def test_candidate_generation_with_ppr_label_enslaved_wikidata():
    random.seed(42)
    OntologyPair.reset()
    preprocessing = Preprocessing("enslaved", "enslaved", "wikidata", relations_to_remove=["disjointWith"])
    preprocessing2 = Preprocessing("enslaved", "enslaved", "wikidata", relations_to_remove=["disjointWith"])
    source_modules, target_modules, sample_target_subgraph = preprocessing.forward(modularizer=PPRModularizer())
    source_modules2, target_modules2, sample_target_subgraph2 = preprocessing2.forward(modularizer=PPRModularizer())
    enslaved_verbalizer = BuildVerbalizer.build("label", "enslaved", "enslaved")
    wikidata_verbalizer = BuildVerbalizer.build("label", "enslaved", "wikidata")
    source_modules = [TextStringVerbalizer().verbalize(enslaved_verbalizer.verbalize(source_module)) for source_module in source_modules]
    target_modules = [TextStringVerbalizer().verbalize(wikidata_verbalizer.verbalize(target_module)) for target_module in target_modules]
    source_modules2 = [TextStringVerbalizer().verbalize(enslaved_verbalizer.verbalize(source_module)) for source_module in source_modules2]
    target_modules2 = [TextStringVerbalizer().verbalize(wikidata_verbalizer.verbalize(target_module)) for target_module in target_modules2]
    cand_generation = CandidateGeneration("embeddinggemma", backend="ollama")
    cand_generation2 = CandidateGeneration("embeddinggemma", backend="ollama")
    result = cand_generation.forward(source_modules, 
                                     target_modules, 
                                     sample_target_subgraph,
                                     preprocessing.ontology_target_path)
    new_result = cand_generation2.forward(source_modules2, 
                                     target_modules2, 
                                     sample_target_subgraph2,
                                     preprocessing2.ontology_target_path)
    for i, res in enumerate(result):
        print(res)
        print(new_result[i])
        assert res[0] == new_result[i][0]
        assert res[1] == new_result[i][1]
    assert result == new_result
    assert type(result) == list
    assert len(result) > 0
    assert any([len(result[i]) > 0 for i in range(len(result))])

def test_candidate_generation_with_ppr_natural():
    OntologyPair.reset()
    preprocessing = Preprocessing("conference", "cmt", "conference", relations_to_remove=["disjointWith"])
    preprocessing2 = Preprocessing("conference", "cmt", "conference", relations_to_remove=["disjointWith"])
    random.seed(42)
    source_modules, target_modules, sample_target_subgraph = preprocessing.forward(modularizer=PPRModularizer())
    random.seed(42)
    source_modules2, target_modules2, sample_target_subgraph2 = preprocessing2.forward(modularizer=PPRModularizer())
    verbalizer = BuildVerbalizer.build("natural", "conference", "cmt")
    source_modules = [TextStringVerbalizer().verbalize(verbalizer.verbalize(source_module)) for source_module in source_modules]
    source_modules2 = [TextStringVerbalizer().verbalize(verbalizer.verbalize(source_module)) for source_module in source_modules2]
    cand_generation = CandidateGeneration("embeddinggemma", backend="ollama")
    cand_generation2 = CandidateGeneration("embeddinggemma", backend="ollama")
    np.random.seed(42)
    result = cand_generation.forward(source_modules,
                                     target_modules,
                                     sample_target_subgraph,
                                     preprocessing.ontology_target_path)
    np.random.seed(42)
    new_result = cand_generation2.forward(source_modules2,
                                     target_modules2,
                                     sample_target_subgraph2,
                                     preprocessing2.ontology_target_path)
    for source in source_modules:
        for triple in source.split("\n"):
            assert len(triple.split()) == 3
    for i, res in enumerate(result):
        assert res[0] == new_result[i][0]
        assert res[1] == new_result[i][1]
    assert result == new_result
    assert type(result) == list
    assert len(result) > 0
    assert any([len(result[i]) > 0 for i in range(len(result))])