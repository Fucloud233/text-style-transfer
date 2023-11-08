# import pandas as pd
from typing import List

from pprint import pprint
from rank_bm25 import BM25Okapi

def read_dataset(path: str):
    with open(path, 'r', encoding="utf-8") as f:
        return f.read(-1).splitlines()

def test():
    train_dataset0_path = 'data/yelp/sentiment.train.0'

    pprint(read_dataset(train_dataset0_path)[:10])

class BM25:
    def __init__(self, corpus: List[str]):
        tokenized_corpus = [doc.split(" ") for doc in corpus]
        self.corpus = corpus
        self.bm25 = BM25Okapi(tokenized_corpus)

    def query_top_n(self, query: str, n: int):
        tokenized_query = query.split(' ')
        # doc_scores = self.bm25.get_scores(tokenized_query)
        return self.bm25.get_top_n(tokenized_query, self.corpus, n=n)
    
    # return only a result
    def query_top_one(self, query: str):
        tokenized_query = query.split(' ')
        return self.bm25.get_top_n(tokenized_query, self.corpus, n=1)[0]
        

if __name__ == '__main__': 
    test()