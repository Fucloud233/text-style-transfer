import sys
sys.path.append('.')

import fasttext

from typing import List

class Classifier:
    def __init__(self, output_path: str):
        self.model = None
        self.output_path = output_path

    def train(self, train_dataset: str, epoch: int=25):
        self.model = fasttext.train_supervised(input=train_dataset, epoch=epoch)
    
    def test(self, test_dataset: str):
        return self.model.test(test_dataset)
    
    def predict(self, sentence: str):
        # extract the result from input
        # e.g. __label__positive
        return self.model.predict(sentence)[0][0][9:]

    def save(self):
        self.model.save_model(self.output_path)

    def load(self):
        # self.model = fasttext.load_model(self.output_path)
        self.model = fasttext.load_model(self.output_path)


# using accuracy instead of score
def evaluate(sentences: List[str],model_path: str,  target_style: str):
    classifier = Classifier(model_path)
    classifier.load()
    
    total = len(sentences)

    counter = 0
    for sentence in sentences:
        kind = classifier.predict(sentence['1'])
        if kind == target_style:
            counter += 1

    return counter / total