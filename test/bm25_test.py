# refs: https://pypi.org/project/rank-bm25/

from rank_bm25 import BM25Okapi


class BM25:
    def __init__(self, corpus: list[str]):
        tokenized_corpus = [doc.split(" ") for doc in corpus]
        self.corpus = corpus
        self.bm25 = BM25Okapi(tokenized_corpus)

    def query(self, query: str):
        tokenized_query = query.split(' ')
        # doc_scores = self.bm25.get_scores(tokenized_query)
        return self.bm25.get_top_n(tokenized_query, self.corpus, n=1)

def test_func():
    corpus = [
        "Hello there good man!",
        "It is quite windy in London",
        "How is the weather today?"
    ]

    query = "windy London"

    bm25 = BM25(corpus)
    print(bm25.query(query))
    

if __name__ == '__main__':
    test_func()

