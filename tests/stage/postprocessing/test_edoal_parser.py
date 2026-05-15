from stage.evaluation.edoal_parser import EDOALParser

def test_edoal_parser():
    edoal_str = EDOALParser().parse("conference", "cmt", "conference")
    with open("reference/conference/cmt-conference.edoal", "r") as f:
        reference = f.read()
    assert edoal_str == reference