from typing import List

from src.model.llama2 import Llama2
from src.bm25 import BM25

class Llama2withBM25(Llama2, BM25):
    def __init__(self, prompt: str, other_dataset: List[str]):
        Llama2.__init__(self, prompt)
        BM25.__init__(self, other_dataset)


    def transfer(self, sentence) -> (str, str):
        similar = self.query_top_one(sentence)
        prompt = self.prompt.format(similar=similar, sentence=sentence)
        return (self._call(prompt), prompt)
