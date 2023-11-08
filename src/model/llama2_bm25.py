from src.model.llama2 import Llama2, LlamaType
from src.bm25 import BM25

class Llama2withBM25(Llama2, BM25):
    def __init__(self, prompt: str, other_dataset: list[str], model_type: LlamaType.Llama_7B_Chat):
        Llama2.__init__(self, prompt, model_type)
        BM25.__init__(self, other_dataset)


    def transfer(self, sentence):
        similar = self.query_top_one(sentence)
        prompt = self.prompt.format(similar=similar, sentence=sentence)
        return self.__call(prompt)
