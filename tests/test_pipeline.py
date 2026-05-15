from pathlib import Path
from omegaconf import DictConfig, OmegaConf
from stage.pipeline import OMPipeline

def get_text_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def test_om_pipeline(monkeypatch):
    from stage.matching.llm_model_vllm import LLMModelVLLM
    from stage.postprocessing.postprocessing import Postprocessing

    def fake_init(self, model_name, cache_dir, dtype, max_model_length, padding_side, max_num_batched_tokens, K, seed):
        pass

    def fake_clean_memory(self):
        pass

    monkeypatch.setattr(LLMModelVLLM, "__init__", fake_init)
    monkeypatch.setattr(LLMModelVLLM, "clean_memory", fake_clean_memory)
    monkeypatch.setattr(LLMModelVLLM, "generate", lambda self, input_texts: [get_text_from_file("tests/edoal_example.txt")])
    monkeypatch.setattr(Postprocessing, "merge_edoals", lambda self, outputs: get_text_from_file("tests/edoal_example.txt"))

    path = Path("stage/config.yaml").resolve()
    # print("Lendo:", path)

    # cfg = OmegaConf.load(path)
    # print(OmegaConf.to_yaml(cfg))

    cfg = OmegaConf.load(path)
    om_pipeline = OMPipeline(cfg)
    om_pipeline.run(42)
    #print("target:", cfg.ontology_target_name)
    #print("verbalizer_type:", cfg.verbalizer_type.matcher)
    print("final_result:", om_pipeline.final_result)
    #print("concept_dict values:", om_pipeline.concept_dict)

    assert type(cfg) == DictConfig
    assert type(om_pipeline.final_result) == str
    assert 'http://edas#AcceptRating' in om_pipeline.concept_dict
    assert 'accept_rating' in om_pipeline.concept_dict.values()
    assert 'http://edas#isWrittenBy' in om_pipeline.concept_dict
    assert 'http://edas#isWrittenBy' in om_pipeline.final_result
    assert 'is_written_by' in om_pipeline.concept_dict.values()
    assert 'is_written_by' not in om_pipeline.final_result
    assert False