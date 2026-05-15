import pytest
from rdflib import OWL, RDF, RDFS, URIRef

from stage.verbalization.label_verbalizer import LabelVerbalizer

@pytest.fixture(scope="module")
def cmt_verbalizer():
    return LabelVerbalizer("datasets/conference/cmt.owl")

@pytest.fixture(scope="module")
def edas_verbalizer():
    return LabelVerbalizer("datasets/conference/edas.owl")

@pytest.fixture(scope="module")
def enslaved_verbalizer():
    return LabelVerbalizer("datasets/enslaved/enslaved.owl")

@pytest.fixture(scope="module")
def taxon_verbalizer():
    return LabelVerbalizer("datasets/taxon/taxon.owl")

def test_verbalize_preference_label(cmt_verbalizer):
    triples = [(URIRef("http://cmt#Preference"), RDF.type, OWL.Class)]
    text = cmt_verbalizer.verbalize(triples)
    assert text == [("Preference", "type", "Class")]
    assert "http://cmt#Preference" in cmt_verbalizer.concept_dict
    assert "Preference" in cmt_verbalizer.concept_dict.values()
    assert str(OWL.Class) in cmt_verbalizer.concept_dict
    assert "Class" in cmt_verbalizer.concept_dict.values()
    assert str(RDF.type) in cmt_verbalizer.concept_dict
    assert "type" in cmt_verbalizer.concept_dict.values()

def test_verbalize_subclass_label(cmt_verbalizer):
    triples = [(URIRef("http://cmt#Meta-Review"), RDFS.subClassOf, URIRef("http://cmt#Review"))]
    text = cmt_verbalizer.verbalize(triples)
    assert text == [("Meta-Review", "subClassOf", "Review")]
    assert "http://cmt#Meta-Review" in cmt_verbalizer.concept_dict
    assert "Meta-Review" in cmt_verbalizer.concept_dict.values()
    assert str(RDFS.subClassOf) in cmt_verbalizer.concept_dict
    assert "subClassOf" in cmt_verbalizer.concept_dict.values()
    assert "http://cmt#Review" in cmt_verbalizer.concept_dict
    assert "Review" in cmt_verbalizer.concept_dict.values()

def test_verbalize_range_label(cmt_verbalizer):
    triples = [(URIRef("http://cmt#adjustBid"), RDFS.range, URIRef("http://cmt#Bid"))]
    text = cmt_verbalizer.verbalize(triples)
    assert text == [("adjustBid", "range", "Bid")]
    assert "http://cmt#adjustBid" in cmt_verbalizer.concept_dict
    assert "adjustBid" in cmt_verbalizer.concept_dict.values()
    assert str(RDFS.range) in cmt_verbalizer.concept_dict
    assert "range" in cmt_verbalizer.concept_dict.values()
    assert "http://cmt#Bid" in cmt_verbalizer.concept_dict
    assert "Bid" in cmt_verbalizer.concept_dict.values()

def test_verbalizer_domain_range_label(cmt_verbalizer):
    triples = [(URIRef("http://cmt#adjustBid"), RDFS.range, URIRef("http://cmt#Bid")), (URIRef("http://cmt#adjustedBy"), RDFS.domain, URIRef("http://cmt#Bid"))]
    text = cmt_verbalizer.verbalize(triples)
    assert text == [("adjustBid", "range", "Bid"), ("adjustedBy", "domain", "Bid")]
    assert "http://cmt#adjustBid" in cmt_verbalizer.concept_dict
    assert "adjustBid" in cmt_verbalizer.concept_dict.values()
    assert "http://cmt#adjustedBy" in cmt_verbalizer.concept_dict
    assert "adjustedBy" in cmt_verbalizer.concept_dict.values()
    assert str(RDFS.range) in cmt_verbalizer.concept_dict
    assert "range" in cmt_verbalizer.concept_dict.values()
    assert "http://cmt#Bid" in cmt_verbalizer.concept_dict
    assert "Bid" in cmt_verbalizer.concept_dict.values()

def test_verbalizer_two_classes_label(edas_verbalizer):
    triples = [(URIRef("http://edas#ConferenceSession"), RDF.type, OWL.Class), (URIRef("http://edas#Review"), RDF.type, OWL.Class)]
    text = edas_verbalizer.verbalize(triples)
    assert text == [("ConferenceSession", "type", "Class"), ("Review", "type", "Class")]
    assert "http://edas#ConferenceSession" in edas_verbalizer.concept_dict
    assert "ConferenceSession" in edas_verbalizer.concept_dict.values()
    assert "http://edas#Review" in edas_verbalizer.concept_dict
    assert "Review" in edas_verbalizer.concept_dict.values()
    assert str(RDF.type) in edas_verbalizer.concept_dict
    assert "type" in edas_verbalizer.concept_dict.values()
    assert str(OWL.Class) in edas_verbalizer.concept_dict
    assert "Class" in edas_verbalizer.concept_dict.values()

def test_verbalizer_taxon_subclass_label(taxon_verbalizer):
    triples = [(URIRef("http://ontology.irstea.fr/agronomictaxon/core#ClassRank"), RDFS.subClassOf, URIRef("http://ontology.irstea.fr/agronomictaxon/core#Taxon"))]
    text = taxon_verbalizer.verbalize(triples)
    assert text == [("Classe", "subClassOf", "Taxon")]
    assert "http://ontology.irstea.fr/agronomictaxon/core#ClassRank" in taxon_verbalizer.concept_dict
    assert "Classe" in taxon_verbalizer.concept_dict.values()
    assert str(RDFS.subClassOf) in taxon_verbalizer.concept_dict
    assert "subClassOf" in taxon_verbalizer.concept_dict.values()
    assert "http://ontology.irstea.fr/agronomictaxon/core#Taxon" in taxon_verbalizer.concept_dict
    assert "Taxon" in taxon_verbalizer.concept_dict.values()

def test_verbalizer_taxon_inverse_of_label(taxon_verbalizer):
    triples = [(URIRef("http://ontology.irstea.fr/agronomictaxon/core#hasHigherRank"), OWL.inverseOf, URIRef("http://ontology.irstea.fr/agronomictaxon/core#hasLowerRank"))]
    text = taxon_verbalizer.verbalize(triples)
    assert text == [("hasHigherRank", "inverseOf", "hasLowerRank")]
    assert "http://ontology.irstea.fr/agronomictaxon/core#hasHigherRank" in taxon_verbalizer.concept_dict
    assert "hasHigherRank" in taxon_verbalizer.concept_dict.values()
    assert str(OWL.inverseOf) in taxon_verbalizer.concept_dict
    assert "inverseOf" in taxon_verbalizer.concept_dict.values()
    assert "http://ontology.irstea.fr/agronomictaxon/core#hasLowerRank" in taxon_verbalizer.concept_dict
    assert "hasLowerRank" in taxon_verbalizer.concept_dict.values()

def test_verbalizer_enslaved_label(enslaved_verbalizer):
    triples = [(URIRef("https://lod.enslaved.org/entity/statement/Q1590-42FE5E4D-8FD1-4FD3-95A6-5725AD0353CB"), RDF.type, URIRef("https://enslaved.org/ontology/NameRecord"))]
    text = enslaved_verbalizer.verbalize(triples)
    assert text == [("Q1590-42FE5E4D-8FD1-4FD3-95A6-5725AD0353CB", "type", "NameRecord")]
    assert "https://lod.enslaved.org/entity/statement/Q1590-42FE5E4D-8FD1-4FD3-95A6-5725AD0353CB" in enslaved_verbalizer.concept_dict
    assert "Q1590-42FE5E4D-8FD1-4FD3-95A6-5725AD0353CB" in enslaved_verbalizer.concept_dict.values()
    assert str(RDF.type) in enslaved_verbalizer.concept_dict
    assert "type" in enslaved_verbalizer.concept_dict.values()
    assert "https://enslaved.org/ontology/NameRecord" in enslaved_verbalizer.concept_dict
    assert "NameRecord" in enslaved_verbalizer.concept_dict.values()

def test_domain_range_conference_label(cmt_verbalizer):
    triples = [(URIRef("http://cmt#hasDecision"), RDFS.domain, URIRef("http://cmt#Paper")), (URIRef("http://cmt#hasDecision"), RDFS.range, URIRef("http://cmt#Decision"))]
    text = cmt_verbalizer.verbalize(triples)
    assert text == [("Paper", "hasDecision", "Decision")]
    assert "http://cmt#Paper" in cmt_verbalizer.concept_dict
    assert "Paper" in cmt_verbalizer.concept_dict.values()
    assert "http://cmt#hasDecision" in cmt_verbalizer.concept_dict
    assert "hasDecision" in cmt_verbalizer.concept_dict.values()
    assert "http://cmt#Decision" in cmt_verbalizer.concept_dict
    assert "Decision" in cmt_verbalizer.concept_dict.values()