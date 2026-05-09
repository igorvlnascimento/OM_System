class AnswerExtractor:
    @staticmethod
    def llm_response(output):
        if output.find('</think>') != -1:
            output = output[output.find('</think>') + len('</think>'):].strip()
        if output.find('```xml') != -1:
            output = output[output.find('```xml') + len('```xml'):].strip()
        if output.find('```') != -1:
            output = output[:output.rfind('```')].strip()
        return output