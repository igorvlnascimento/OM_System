import pytest
from rdflib import OWL, RDF, RDFS, URIRef

from stage.verbalization.label_verbalizer import LabelVerbalizer
from stage.verbalization.natural_verbalizer import DefaultStrategy, EquivalentClassStrategy, InverseOfStrategy, NaturalVerbalizer, SubClassOfStrategy, SubPropertyOfStrategy, TypeStrategy

STRATEGIES = [
    SubClassOfStrategy(),
    SubPropertyOfStrategy(),
    TypeStrategy(),
    EquivalentClassStrategy(),
    InverseOfStrategy(),
    DefaultStrategy(),
]

@pytest.fixture(scope="module")
def cmt_verbalizer():
    verbalizer = LabelVerbalizer("datasets/conference/cmt.owl")
    return NaturalVerbalizer(verbalizer, STRATEGIES)

@pytest.fixture(scope="module")
def edas_verbalizer():
    verbalizer = LabelVerbalizer("datasets/conference/edas.owl")
    return NaturalVerbalizer(verbalizer, STRATEGIES)

@pytest.fixture(scope="module")
def enslaved_verbalizer():
    verbalizer = LabelVerbalizer("datasets/enslaved/enslaved.owl")
    return NaturalVerbalizer(verbalizer, STRATEGIES)

@pytest.fixture(scope="module")
def taxon_verbalizer():
    verbalizer = LabelVerbalizer("datasets/taxon/taxon.owl")
    return NaturalVerbalizer(verbalizer, STRATEGIES)

def test_verbalize_preference_label(cmt_verbalizer):
    triples = [(URIRef("http://cmt#Preference"), RDF.type, OWL.Class)]
    text = cmt_verbalizer.verbalize(triples)
    assert text == [("preference", "is_type_of", "class")]
    assert "http://cmt#Preference" in cmt_verbalizer.concept_dict
    assert "preference" in cmt_verbalizer.concept_dict.values()
    assert str(OWL.Class) in cmt_verbalizer.concept_dict
    assert "class" in cmt_verbalizer.concept_dict.values()
    assert str(RDF.type) in cmt_verbalizer.concept_dict
    assert "is_type_of" in cmt_verbalizer.concept_dict.values()

def test_verbalize_subclass_label(cmt_verbalizer):
    triples = [(URIRef("http://cmt#Meta-Review"), RDFS.subClassOf, URIRef("http://cmt#Review"))]
    text = cmt_verbalizer.verbalize(triples)
    assert text == [("meta-review", "is_a", "review")]
    assert "http://cmt#Meta-Review" in cmt_verbalizer.concept_dict
    assert "meta-review" in cmt_verbalizer.concept_dict.values()
    assert "http://cmt#Review" in cmt_verbalizer.concept_dict
    assert "review" in cmt_verbalizer.concept_dict.values()
    assert str(RDFS.subClassOf) in cmt_verbalizer.concept_dict
    assert "is_a" in cmt_verbalizer.concept_dict.values()

def test_verbalize_range_label(cmt_verbalizer):
    triples = [(URIRef("http://cmt#adjustBid"), RDFS.range, URIRef("http://cmt#Bid"))]
    text = cmt_verbalizer.verbalize(triples)
    assert text == [("adjust_bid", "range", "bid")]
    assert "http://cmt#adjustBid" in cmt_verbalizer.concept_dict
    assert "adjust_bid" in cmt_verbalizer.concept_dict.values()
    assert "http://cmt#Bid" in cmt_verbalizer.concept_dict
    assert "bid" in cmt_verbalizer.concept_dict.values()
    assert str(RDFS.range) in cmt_verbalizer.concept_dict
    assert "range" in cmt_verbalizer.concept_dict.values()

def test_verbalizer_domain_range_label(cmt_verbalizer):
    triples = [(URIRef("http://cmt#adjustBid"), RDFS.range, URIRef("http://cmt#Bid")), (URIRef("http://cmt#adjustedBy"), RDFS.domain, URIRef("http://cmt#Bid"))]
    text = cmt_verbalizer.verbalize(triples)
    assert text == [("adjust_bid", "range", "bid"), ("adjusted_by", "domain", "bid")]
    assert "http://cmt#adjustBid" in cmt_verbalizer.concept_dict
    assert "adjust_bid" in cmt_verbalizer.concept_dict.values()
    assert "http://cmt#Bid" in cmt_verbalizer.concept_dict
    assert "bid" in cmt_verbalizer.concept_dict.values()
    assert "http://cmt#adjustedBy" in cmt_verbalizer.concept_dict
    assert "adjusted_by" in cmt_verbalizer.concept_dict.values()
    assert str(RDFS.range) in cmt_verbalizer.concept_dict
    assert "range" in cmt_verbalizer.concept_dict.values()
    assert str(RDFS.domain) in cmt_verbalizer.concept_dict
    assert "domain" in cmt_verbalizer.concept_dict.values()

def test_verbalizer_two_classes_label(edas_verbalizer):
    triples = [(URIRef("http://edas#ConferenceSession"), RDF.type, OWL.Class), (URIRef("http://edas#Review"), RDF.type, OWL.Class)]
    text = edas_verbalizer.verbalize(triples)
    assert text == [("conference_session", "is_type_of", "class"), ("review", "is_type_of", "class")]
    assert "http://edas#ConferenceSession" in edas_verbalizer.concept_dict
    assert "conference_session" in edas_verbalizer.concept_dict.values()
    assert "http://edas#Review" in edas_verbalizer.concept_dict
    assert "review" in edas_verbalizer.concept_dict.values()
    assert str(RDF.type) in edas_verbalizer.concept_dict
    assert "is_type_of" in edas_verbalizer.concept_dict.values()
    assert str(OWL.Class) in edas_verbalizer.concept_dict
    assert "class" in edas_verbalizer.concept_dict.values()

def test_verbalizer_taxon_subclass_label(taxon_verbalizer):
    triples = [(URIRef("http://ontology.irstea.fr/agronomictaxon/core#ClassRank"), RDFS.subClassOf, URIRef("http://ontology.irstea.fr/agronomictaxon/core#Taxon"))]
    text = taxon_verbalizer.verbalize(triples)
    assert text == [("classe", "is_a", "taxon")]
    assert "http://ontology.irstea.fr/agronomictaxon/core#ClassRank" in taxon_verbalizer.concept_dict
    assert "classe" in taxon_verbalizer.concept_dict.values()
    assert str(RDFS.subClassOf) in taxon_verbalizer.concept_dict
    assert "is_a" in taxon_verbalizer.concept_dict.values()
    assert "http://ontology.irstea.fr/agronomictaxon/core#Taxon" in taxon_verbalizer.concept_dict
    assert "taxon" in taxon_verbalizer.concept_dict.values()

def test_verbalizer_taxon_inverse_of_label(taxon_verbalizer):
    triples = [(URIRef("http://ontology.irstea.fr/agronomictaxon/core#hasHigherRank"), OWL.inverseOf, URIRef("http://ontology.irstea.fr/agronomictaxon/core#hasLowerRank"))]
    text = taxon_verbalizer.verbalize(triples)
    assert text == [("has_higher_rank", "is_inverse_of", "has_lower_rank")]
    assert "http://ontology.irstea.fr/agronomictaxon/core#hasHigherRank" in taxon_verbalizer.concept_dict
    assert "has_higher_rank" in taxon_verbalizer.concept_dict.values()
    assert str(OWL.inverseOf) in taxon_verbalizer.concept_dict
    assert "is_inverse_of" in taxon_verbalizer.concept_dict.values()
    assert "http://ontology.irstea.fr/agronomictaxon/core#hasLowerRank" in taxon_verbalizer.concept_dict
    assert "has_lower_rank" in taxon_verbalizer.concept_dict.values()

def test_verbalizer_enslaved_label(enslaved_verbalizer):
    triples = [(URIRef("https://lod.enslaved.org/entity/statement/Q1590-42FE5E4D-8FD1-4FD3-95A6-5725AD0353CB"), RDF.type, URIRef("https://enslaved.org/ontology/NameRecord"))]
    text = enslaved_verbalizer.verbalize(triples)
    assert text == [("q1590-42fe5e4d-8fd1-4fd3-95a6-5725ad0353cb", "is_type_of", "name_record")]
    assert "https://lod.enslaved.org/entity/statement/Q1590-42FE5E4D-8FD1-4FD3-95A6-5725AD0353CB" in enslaved_verbalizer.concept_dict
    assert "q1590-42fe5e4d-8fd1-4fd3-95a6-5725ad0353cb" in enslaved_verbalizer.concept_dict.values()
    assert str(RDF.type) in enslaved_verbalizer.concept_dict
    assert "is_type_of" in enslaved_verbalizer.concept_dict.values()
    assert "https://enslaved.org/ontology/NameRecord" in enslaved_verbalizer.concept_dict
    assert "name_record" in enslaved_verbalizer.concept_dict.values()

def test_domain_range_conference_label(cmt_verbalizer):
    triples = [(URIRef("http://cmt#hasDecision"), RDFS.domain, URIRef("http://cmt#Paper")), (URIRef("http://cmt#hasDecision"), RDFS.range, URIRef("http://cmt#Decision"))]
    text = cmt_verbalizer.verbalize(triples)
    assert text == [("paper", "has_decision", "decision")]
    assert "http://cmt#Paper" in cmt_verbalizer.concept_dict
    assert "paper" in cmt_verbalizer.concept_dict.values()
    assert "http://cmt#hasDecision" in cmt_verbalizer.concept_dict
    assert "has_decision" in cmt_verbalizer.concept_dict.values()
    assert "http://cmt#Decision" in cmt_verbalizer.concept_dict
    assert "decision" in cmt_verbalizer.concept_dict.values()


