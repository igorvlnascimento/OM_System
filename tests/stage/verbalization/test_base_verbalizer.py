import pytest
from rdflib import OWL, RDF, RDFS, URIRef

from stage.verbalization.base_verbalizer import BaseVerbalizer

@pytest.fixture(scope="module")
def cmt_verbalizer():
    return BaseVerbalizer("datasets/conference/cmt.owl")

@pytest.fixture(scope="module")
def edas_verbalizer():
    return BaseVerbalizer("datasets/conference/edas.owl")

@pytest.fixture(scope="module")
def enslaved_verbalizer():
    return BaseVerbalizer("datasets/enslaved/enslaved.owl")

@pytest.fixture(scope="module")
def taxon_verbalizer():
    return BaseVerbalizer("datasets/taxon/taxon.owl")

def test_verbalize_preference_base(cmt_verbalizer):
    triples = [(URIRef("http://cmt#Preference"), RDF.type, OWL.Class)]
    text = cmt_verbalizer.verbalize(triples)
    assert text == [("http://cmt#Preference", str(RDF.type), str(OWL.Class))]
    assert "http://cmt#Preference" in cmt_verbalizer.concept_dict
    assert "http://cmt#Preference" in cmt_verbalizer.concept_dict.values()
    assert str(OWL.Class) in cmt_verbalizer.concept_dict
    assert str(OWL.Class) in cmt_verbalizer.concept_dict.values()
    assert str(RDF.type) in cmt_verbalizer.concept_dict
    assert str(RDF.type) in cmt_verbalizer.concept_dict.values()

def test_verbalize_subclass_base(cmt_verbalizer):
    triples = [(URIRef("http://cmt#Meta-Review"), RDFS.subClassOf, URIRef("http://cmt#Review"))]
    text = cmt_verbalizer.verbalize(triples)
    assert text == [("http://cmt#Meta-Review", str(RDFS.subClassOf), "http://cmt#Review")]
    assert "http://cmt#Meta-Review" in cmt_verbalizer.concept_dict
    assert "http://cmt#Meta-Review" in cmt_verbalizer.concept_dict.values()
    assert str(RDFS.subClassOf) in cmt_verbalizer.concept_dict
    assert str(RDFS.subClassOf) in cmt_verbalizer.concept_dict.values()
    assert "http://cmt#Review" in cmt_verbalizer.concept_dict
    assert "http://cmt#Review" in cmt_verbalizer.concept_dict.values()

def test_verbalize_range_base(cmt_verbalizer):
    triples = [(URIRef("http://cmt#adjustBid"), RDFS.range, URIRef("http://cmt#Bid"))]
    text = cmt_verbalizer.verbalize(triples)
    assert text == [("http://cmt#adjustBid", str(RDFS.range), "http://cmt#Bid")]
    assert "http://cmt#adjustBid" in cmt_verbalizer.concept_dict
    assert "http://cmt#adjustBid" in cmt_verbalizer.concept_dict.values()
    assert "http://cmt#Bid" in cmt_verbalizer.concept_dict
    assert "http://cmt#Bid" in cmt_verbalizer.concept_dict.values()
    assert str(RDFS.range) in cmt_verbalizer.concept_dict
    assert str(RDFS.range) in cmt_verbalizer.concept_dict.values()

def test_verbalizer_domain_range_base(cmt_verbalizer):
    triples = [(URIRef("http://cmt#adjustBid"), RDFS.range, URIRef("http://cmt#Bid")), (URIRef("http://cmt#adjustedBy"), RDFS.domain, URIRef("http://cmt#Bid"))]
    text = cmt_verbalizer.verbalize(triples)
    assert text == [("http://cmt#adjustBid", str(RDFS.range), "http://cmt#Bid"), ("http://cmt#adjustedBy", str(RDFS.domain), "http://cmt#Bid")]
    assert "http://cmt#adjustBid" in cmt_verbalizer.concept_dict
    assert "http://cmt#adjustBid" in cmt_verbalizer.concept_dict.values()
    assert "http://cmt#Bid" in cmt_verbalizer.concept_dict
    assert "http://cmt#Bid" in cmt_verbalizer.concept_dict.values()
    assert "http://cmt#adjustedBy" in cmt_verbalizer.concept_dict
    assert "http://cmt#adjustedBy" in cmt_verbalizer.concept_dict.values()
    assert str(RDFS.range) in cmt_verbalizer.concept_dict
    assert str(RDFS.range) in cmt_verbalizer.concept_dict.values()
    assert str(RDFS.domain) in cmt_verbalizer.concept_dict
    assert str(RDFS.domain) in cmt_verbalizer.concept_dict.values()

def test_verbalizer_two_classes_base(edas_verbalizer):
    triples = [(URIRef("http://edas#ConferenceSession"), RDF.type, OWL.Class), (URIRef("http://edas#Review"), RDF.type, OWL.Class)]
    text = edas_verbalizer.verbalize(triples)
    assert text == [("http://edas#ConferenceSession", str(RDF.type), str(OWL.Class)), ("http://edas#Review", str(RDF.type), str(OWL.Class))]
    assert "http://edas#ConferenceSession" in edas_verbalizer.concept_dict
    assert "http://edas#ConferenceSession" in edas_verbalizer.concept_dict.values()
    assert "http://edas#Review" in edas_verbalizer.concept_dict
    assert "http://edas#Review" in edas_verbalizer.concept_dict.values()
    assert str(RDF.type) in edas_verbalizer.concept_dict
    assert str(RDF.type) in edas_verbalizer.concept_dict.values()
    assert str(OWL.Class) in edas_verbalizer.concept_dict
    assert str(OWL.Class) in edas_verbalizer.concept_dict.values()

def test_verbalizer_taxon_subclass_base(taxon_verbalizer):
    triples = [(URIRef("http://ontology.irstea.fr/agronomictaxon/core#ClassRank"), RDFS.subClassOf, URIRef("http://ontology.irstea.fr/agronomictaxon/core#Taxon"))]
    text = taxon_verbalizer.verbalize(triples)
    assert text == [("http://ontology.irstea.fr/agronomictaxon/core#ClassRank", str(RDFS.subClassOf), "http://ontology.irstea.fr/agronomictaxon/core#Taxon")]
    assert "http://ontology.irstea.fr/agronomictaxon/core#ClassRank" in taxon_verbalizer.concept_dict
    assert "http://ontology.irstea.fr/agronomictaxon/core#ClassRank" in taxon_verbalizer.concept_dict.values()
    assert str(RDFS.subClassOf) in taxon_verbalizer.concept_dict
    assert str(RDFS.subClassOf) in taxon_verbalizer.concept_dict.values()
    assert "http://ontology.irstea.fr/agronomictaxon/core#Taxon" in taxon_verbalizer.concept_dict
    assert "http://ontology.irstea.fr/agronomictaxon/core#Taxon" in taxon_verbalizer.concept_dict.values()

def test_verbalizer_taxon_inverse_of_base(taxon_verbalizer):
    triples = [(URIRef("http://ontology.irstea.fr/agronomictaxon/core#hasHigherRank"), OWL.inverseOf, URIRef("http://ontology.irstea.fr/agronomictaxon/core#hasLowerRank"))]
    text = taxon_verbalizer.verbalize(triples)
    assert text == [("http://ontology.irstea.fr/agronomictaxon/core#hasHigherRank", str(OWL.inverseOf), "http://ontology.irstea.fr/agronomictaxon/core#hasLowerRank")]
    assert "http://ontology.irstea.fr/agronomictaxon/core#hasHigherRank" in taxon_verbalizer.concept_dict
    assert "http://ontology.irstea.fr/agronomictaxon/core#hasHigherRank" in taxon_verbalizer.concept_dict.values()
    assert str(OWL.inverseOf) in taxon_verbalizer.concept_dict
    assert str(OWL.inverseOf) in taxon_verbalizer.concept_dict.values()
    assert "http://ontology.irstea.fr/agronomictaxon/core#hasLowerRank" in taxon_verbalizer.concept_dict
    assert "http://ontology.irstea.fr/agronomictaxon/core#hasLowerRank" in taxon_verbalizer.concept_dict.values()

def test_verbalizer_enslaved_base(enslaved_verbalizer):
    triples = [(URIRef("https://lod.enslaved.org/entity/statement/Q1590-42FE5E4D-8FD1-4FD3-95A6-5725AD0353CB"), RDF.type, URIRef("https://enslaved.org/ontology/NameRecord"))]
    text = enslaved_verbalizer.verbalize(triples)
    assert text == [("https://lod.enslaved.org/entity/statement/Q1590-42FE5E4D-8FD1-4FD3-95A6-5725AD0353CB", str(RDF.type), "https://enslaved.org/ontology/NameRecord")]
    assert "https://lod.enslaved.org/entity/statement/Q1590-42FE5E4D-8FD1-4FD3-95A6-5725AD0353CB" in enslaved_verbalizer.concept_dict
    assert "https://lod.enslaved.org/entity/statement/Q1590-42FE5E4D-8FD1-4FD3-95A6-5725AD0353CB" in enslaved_verbalizer.concept_dict.values()
    assert str(RDF.type) in enslaved_verbalizer.concept_dict
    assert str(RDF.type) in enslaved_verbalizer.concept_dict.values()
    assert "https://enslaved.org/ontology/NameRecord" in enslaved_verbalizer.concept_dict
    assert "https://enslaved.org/ontology/NameRecord" in enslaved_verbalizer.concept_dict.values()

def test_domain_range_conference_base(cmt_verbalizer):
    triples = [(URIRef("http://cmt#hasDecision"), RDFS.domain, URIRef("http://cmt#Paper")), (URIRef("http://cmt#hasDecision"), RDFS.range, URIRef("http://cmt#Decision"))]
    text = cmt_verbalizer.verbalize(triples)
    assert text == [("http://cmt#Paper", "http://cmt#hasDecision", "http://cmt#Decision")]
    assert "http://cmt#Paper" in cmt_verbalizer.concept_dict
    assert "http://cmt#Paper" in cmt_verbalizer.concept_dict.values()
    assert "http://cmt#hasDecision" in cmt_verbalizer.concept_dict
    assert "http://cmt#hasDecision" in cmt_verbalizer.concept_dict.values()
    assert "http://cmt#Decision" in cmt_verbalizer.concept_dict
    assert "http://cmt#Decision" in cmt_verbalizer.concept_dict.values()
