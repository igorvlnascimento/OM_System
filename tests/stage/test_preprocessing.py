import random

from rdflib import OWL
from stage.modularization.modularizer import PPRModularizer
from stage.preprocessing.ontology_pair import OntologyPair
from stage.preprocessing.preprocessing import Preprocessing
from stage.verbalization.build_verbalizer import BuildVerbalizer


def test_preprocessing_baseline():
    random.seed(42)
    preprocess = Preprocessing("conference", "cmt", "conference")
    preprocess2 = Preprocessing("conference", "cmt", "conference")
    source_modules, target_modules, sample_target_modules = preprocess.forward()
    source_modules2, target_modules2, sample_target_modules2 = preprocess2.forward()
    for triple in source_modules[0]:
        assert OWL.Class not in triple
    for triple in target_modules[0]:
        assert OWL.Class not in triple
    for triple in source_modules2[0]:
        assert OWL.Class not in triple
    for triple in target_modules2[0]:
        assert OWL.Class not in triple
    assert source_modules[0] == source_modules2[0]
    assert target_modules[0] == target_modules2[0]
    assert sample_target_modules[0] == sample_target_modules2[0]
    assert type(source_modules[0][0]) == tuple
    assert type(source_modules2[0][0]) == tuple
    assert type(target_modules[0][0]) == tuple
    assert type(target_modules2[0][0]) == tuple
    assert type(sample_target_modules[0][0]) == str
    assert type(sample_target_modules2[0][0]) == str
    assert source_modules[0][0][0].find("@prefix") == -1
    assert source_modules[0][0][0].find("http://") == 0

def test_preprocessing_ppr():
    preprocess = Preprocessing("conference", "cmt", "conference")
    preprocess2 = Preprocessing("conference", "cmt", "conference")
    source_modules, target_modules, sample_target_modules = preprocess.forward(modularizer=PPRModularizer())
    source_modules2, target_modules2, sample_target_modules2 = preprocess2.forward(modularizer=PPRModularizer())
    for triple in source_modules[0]:
        assert OWL.Class not in triple
    for triple in target_modules[0]:
        assert OWL.Class not in triple
    for triple in source_modules2[0]:
        assert OWL.Class not in triple
    for triple in target_modules2[0]:
        assert OWL.Class not in triple
    assert source_modules[0] == source_modules2[0]
    assert target_modules[0] == target_modules2[0]
    assert sample_target_modules[0] == sample_target_modules2[0]
    assert type(source_modules[0][0]) == tuple
    assert type(source_modules2[0][0]) == tuple
    assert type(target_modules[0][0]) == tuple
    assert type(target_modules2[0][0]) == tuple
    assert type(sample_target_modules[0][0]) == str
    assert type(sample_target_modules2[0][0]) == str
    assert str(source_modules[0][0][0]).find("@prefix") == -1
    assert str(source_modules[0][0][0]).find("http://") == 0


def test_preprocessing_baseline_label():
    preprocess = Preprocessing("conference", "cmt", "conference")
    preprocess2 = Preprocessing("conference", "cmt", "conference")
    source_modules, target_modules, sample_target_modules = preprocess.forward()
    for triple in source_modules[0]:
        assert OWL.Class not in triple
    for triple in target_modules[0]:
        assert OWL.Class not in triple
    cmt_verbalizer = BuildVerbalizer.build("label", "conference", "cmt")
    conference_verbalizer = BuildVerbalizer.build("label", "conference", "conference")
    source_modules = [cmt_verbalizer.verbalize(module) for module in source_modules]
    target_modules = [conference_verbalizer.verbalize(module) for module in target_modules]
    source_modules2, target_modules2, sample_target_modules2 = preprocess2.forward()
    for triple in source_modules2[0]:
        assert OWL.Class not in triple
    for triple in target_modules2[0]:
        assert OWL.Class not in triple
    assert "http://cmt#adjustBid" in cmt_verbalizer.concept_dict
    assert "adjustBid" in cmt_verbalizer.concept_dict.values()
    assert source_modules[0] != source_modules2[0]
    assert target_modules[0] != target_modules2[0]
    assert sample_target_modules[0] == sample_target_modules2[0]
    assert type(source_modules[0][0]) == tuple
    assert type(source_modules2[0][0]) == tuple
    assert type(target_modules[0][0]) == tuple
    assert type(target_modules2[0][0]) == tuple
    assert type(sample_target_modules[0][0]) == str
    assert type(sample_target_modules2[0][0]) == str
    assert str(source_modules[0][0][0]).find("@prefix") == -1
    assert str(source_modules[0][0][0]).find("http://") == -1
    assert str(target_modules[0][0][0]).find("@prefix") == -1
    assert str(target_modules[0][0][0]).find("http://") == -1

def test_preprocessing_ppr_label():
    preprocess = Preprocessing("conference", "cmt", "conference")
    preprocess2 = Preprocessing("conference", "cmt", "conference")
    source_modules, target_modules, sample_target_modules = preprocess.forward(modularizer=PPRModularizer())
    for triple in source_modules[0]:
        assert OWL.Class not in triple
    for triple in target_modules[0]:
        assert OWL.Class not in triple
    cmt_verbalizer = BuildVerbalizer.build("label", "conference", "cmt")
    conference_verbalizer = BuildVerbalizer.build("label", "conference", "conference")
    source_modules = [cmt_verbalizer.verbalize(module) for module in source_modules]
    target_modules = [conference_verbalizer.verbalize(module) for module in target_modules]
    source_modules2, target_modules2, sample_target_modules2 = preprocess2.forward(modularizer=PPRModularizer())
    assert "http://cmt#adjustBid" in cmt_verbalizer.concept_dict
    assert "adjustBid" in cmt_verbalizer.concept_dict.values()
    assert source_modules[0] != source_modules2[0]
    assert target_modules[0] != target_modules2[0]
    assert sample_target_modules[0] == sample_target_modules2[0]
    assert type(source_modules[0][0]) == tuple
    assert type(source_modules2[0][0]) == tuple
    assert type(target_modules[0][0]) == tuple
    assert type(target_modules2[0][0]) == tuple
    assert type(sample_target_modules[0][0]) == str
    assert type(sample_target_modules2[0][0]) == str
    assert str(source_modules[0][0][0]).find("http://") == -1
    assert str(target_modules[0][0][0]).find("http://") == -1
    assert str(source_modules2[0][0][0]).find("http://") == 0
    assert str(target_modules2[0][0][0]).find("http://") == 0

def test_preprocessing_ppr_label_enslaved_wikidata():
    OntologyPair.reset()
    preprocess = Preprocessing("enslaved", "enslaved", "wikidata")
    preprocess2 = Preprocessing("enslaved", "enslaved", "wikidata")
    source_modules, target_modules, sample_target_modules = preprocess.forward(modularizer=PPRModularizer())
    for triple in source_modules[0]:
        assert OWL.Class not in triple
    for triple in target_modules[0]:
        assert OWL.Class not in triple
    enslaved_verbalizer = BuildVerbalizer.build("label", "enslaved", "enslaved")
    wikidata_verbalizer = BuildVerbalizer.build("label", "enslaved", "wikidata")
    source_modules = [enslaved_verbalizer.verbalize(module) for module in source_modules]
    target_modules = [wikidata_verbalizer.verbalize(module) for module in target_modules]
    source_modules2, target_modules2, sample_target_modules2 = preprocess2.forward(modularizer=PPRModularizer())
    assert "https://enslaved.org/ontology/Description" in enslaved_verbalizer.concept_dict
    assert "Description" in enslaved_verbalizer.concept_dict.values()
    assert source_modules[0] != source_modules2[0]
    assert target_modules[0] == target_modules2[0]
    assert sample_target_modules[0] == sample_target_modules2[0]
    assert type(source_modules[0][0]) == tuple
    assert type(source_modules2[0][0]) == tuple
    assert type(target_modules[0]) == list
    assert type(target_modules2[0]) == list
    assert type(sample_target_modules[0][0]) == str
    assert type(sample_target_modules2[0][0]) == str
    assert str(source_modules[0][0][0]).find("http://") == -1
    assert len(target_modules[0]) == 0
    assert str(source_modules2[0][0][0]).find("https://") == 0
    assert len(target_modules2[0]) == 0