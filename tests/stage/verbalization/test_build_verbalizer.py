from stage.verbalization.build_verbalizer import BuildVerbalizer


def test_build_natural_edas_verbalizer():
    edas_verbalizer = BuildVerbalizer.build("natural", "conference", "edas")
    assert 'http://edas#AcceptRating' in edas_verbalizer.concept_dict
    assert 'accept_rating' in edas_verbalizer.concept_dict.values()

def test_build_label_edas_verbalizer():
    edas_verbalizer = BuildVerbalizer.build("label", "conference", "edas")
    assert 'http://edas#AcceptRating' in edas_verbalizer.concept_dict
    assert 'AcceptRating' in edas_verbalizer.concept_dict.values()
