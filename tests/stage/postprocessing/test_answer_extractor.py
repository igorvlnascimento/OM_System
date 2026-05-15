from stage.postprocessing.answer_extractor import AnswerExtractor


def test_extractor_simple():
    llm_response = '''<think>Estou pensando</think>
    Agora vou dar a resposta
    '''
    assert AnswerExtractor.llm_response(llm_response) == 'Agora vou dar a resposta'


def test_extractor_text_with_xml():
    llm_response = '''``xml
    <think>Estou pensando</think>
    Agora vou dar a resposta
    ```
    '''
    assert AnswerExtractor.llm_response(llm_response) == 'Agora vou dar a resposta'
    