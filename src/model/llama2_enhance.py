import random 
from typing import List

from src.model.llama2 import Llama2
from bm25 import BM25

class Llama2withBM25(Llama2, BM25):
    def __init__(self, prompt: str, other_dataset: List[str]):
        Llama2.__init__(self, prompt)
        BM25.__init__(self, other_dataset)


    def transfer(self, sentence) -> (str, str):
        similar = self.query_top_one(sentence)
        prompt = self.prompt.format(similar=similar, sentence=sentence)
        return (self._call(prompt), prompt)

class Llama2WithRandom(Llama2):
    def __init__(self, prompt: str, other_dataset: List[str]):
        random.seed(2017)

        Llama2.__init__(self, prompt)

        self.other_dataset = other_dataset   

    def transfer(self, sentence):
        # random sample one data from dataset
        random_sample = random.sample(self.other_dataset, 1)
        prompt = self.prompt.format(similar=random_sample, sentence=sentence)     
        return (self._call(prompt), prompt)   