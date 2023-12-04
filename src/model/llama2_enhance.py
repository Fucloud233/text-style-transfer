import random 
from typing import List
from abc import abstractmethod

from src.model.llama2 import Llama2, add_division
from src.model.bm25 import BM25
from utils.config import RetrievalType

# the base class of the llama2 with retrieval
class Llama2Retrieval(Llama2):

    def __init__(self, type: RetrievalType, prompt: str=None):
        Llama2.__init__(self, prompt)
        self._type = type
        
    @abstractmethod
    def _retrieval(self, sentence: str, retrieval_num: str) -> str | List[str]:
        pass

    def transfer(self, sentence: str, target_style: str, retrieval_num: int) -> (str, str):
        similar = self._retrieval(sentence, retrieval_num)
        
        # append division for sentence
        if isinstance(similar, str):
            similar = add_division(similar)
        else:
            similar = '\n'.join([ add_division(s) for s in similar ])

        prompt = self._prompt.format(similar=similar, sentence=add_division(sentence), target=target_style)
        return (self._call(prompt), prompt)

# Random
class Llama2WithRandom(Llama2Retrieval):
    def __init__(self, other_dataset: List[str], prompt: str=None):
        Llama2Retrieval.__init__(self, RetrievalType.Random, prompt)
        random.seed(2017)
        self.other_dataset = other_dataset   

    def _retrieval(self, _sentence: str, retrieval_num: int) -> str:
        return random.sample(self.other_dataset, retrieval_num)

# BM25
class Llama2withBM25(Llama2Retrieval, BM25):
    def __init__(self, other_dataset: List[str], prompt: str=None):
        Llama2Retrieval.__init__(self, RetrievalType.BM25, prompt)
        BM25.__init__(self, other_dataset)
    
    def _retrieval(self, sentence: str, retrieval_num: int) -> str:
        return self.query_top_n(sentence, retrieval_num)

# GTR
class Llama2withGTR(Llama2Retrieval):
    def __init__(self, dataset_name: str, prompt: str=None):
        Llama2Retrieval.__init__(self, RetrievalType.GTR, prompt)

        from src.model.chroma import VectorDB

        self.db = VectorDB()
        self.dataset_name = dataset_name
    
    def _retrieval(self, sentence: str, retrieval_num: int) -> str:
        return self.db.query(self.dataset_name, sentence, retrieval_num)