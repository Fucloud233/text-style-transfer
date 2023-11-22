import sys; sys.path.append(".")

import random
import chromadb
from chromadb.utils import embedding_functions
from chromadb.api.models.Collection import Collection
from tqdm import tqdm
from typing import List

from utils.file import read_lines

random.seed(2017)

def test_try():
    from sentence_transformers import SentenceTransformer, util

    import torch

    # https://huggingface.co/sentence-transformers/gtr-t5-base
    # https://huggingface.co/tasks/sentence-similarity

    # 1. get the model
    model = SentenceTransformer('sentence-transformers/gtr-t5-base')
    
    # 2. embedding source sentences
    source = 'That is a happy person'
    source_embedding = model.encode(source, convert_to_tensor=True)

    # 3. embedding target sentences
    targets = [
        "That is a happy dog",
        "That is a very happy person",
        "Today is a sunny day"
    ]
    target_embeddings = model.encode(targets, convert_to_tensor=True)

    # 4. calculate the cosine similarity
    distances = util.pytorch_cos_sim(source_embedding, target_embeddings)
    
    # 5. find the most similar
    i = torch.argmax(distances)
    print(targets[i])
    
class VectorDB:
    def __init__(self):
        self.client = chromadb.PersistentClient(path='model/chroma')

        self.embedding_function = embedding_functions \
            .SentenceTransformerEmbeddingFunction(model_name='gtr-t5-base')
        
        # reload the name of collections in-memory
        self.collections = {}
        for collection in self.get_collections_list():
            self.collections[collection] = \
                self.client.get_collection(collection, embedding_function=self.embedding_function)                    

    def init_collection(self, name: str, k: int=-1):
        # 1. reload dataset
        dataset_path = "data/{}/train.1".format(name)
        lines = read_lines(dataset_path)
        lines = lines[:k] if k != -1 else lines

        # 2. create collection and add documents
        collection = self.client.create_collection(name, embedding_function=self.embedding_function)
        for (i, sentence) in tqdm(list(enumerate(lines)), desc="Embedding Process"):
            collection.add(documents=[sentence], ids=[str(i)])

        # 3. record in dictionary
        self.collections[name] = collection
    
    def delete_collection(self, name: str):
        try:
            self.client.delete_collection(name)
        except ValueError:
            # if the collections not exists
            pass
    
    def query(self, name: str, sentence: str, k: int=1):
        collection: Collection = self.collections[name]

        result = collection.query(
            query_texts=[sentence],
            n_results=k
        )

        return result['documents'][0]


    def get_collections_list(self) -> List[str]:
        return [collection.name for collection in self.client.list_collections()]
    
    def display(self, name: str):
        collection = self.__get_collection(name)
        print(collection.get())
        print(collection.id)
        print(collection.count())


    def __get_collection(self, name: str) -> Collection:
        return self.collections[name]        

def test():
    collection_name = 'yelp'

    db = VectorDB()

    # db.delete_collection(collection_name)

    # db.init_collection(collection_name)

    # print(db.query(collection_name, collection_name))

    db.display(collection_name)

if __name__ == '__main__':
    test()
