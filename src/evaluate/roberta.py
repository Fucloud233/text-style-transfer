import sys; sys.path.append(".")
import os; os.environ['CURL_CA_BUNDLE'] = ''


from typing import List
from tqdm import tqdm
from transformers import pipeline
from transformers import RobertaTokenizer

from collections import Counter

from utils.file import load_test_cases


# MODEL_PATH = "model/roberta/"
REPOSITORY_ID = 'roberta-large'

def get_target_label(style_id: int):
    return 'LABEL_{}'.format(style_id)

class Classifier:
    tokenizer = RobertaTokenizer.from_pretrained(REPOSITORY_ID)
    
    __model_path_template = 'model/roberta-{}'

    def __init__(self, dataset_name: str, model_path: str=None):
        self.dataset_name = dataset_name
        self.model_path = model_path if model_path != None \
            else Classifier.__model_path_template.format(dataset_name)

        self.classifier = pipeline(
            task="text-classification",
            model=self.model_path,
            tokenizer=Classifier.tokenizer,
            device='cpu'
        )
    
    def predict(self, sentence: str, style_id: int) -> bool:
        result = self.classifier(sentence)
        target_label = get_target_label(style_id)
        return result[0]['label'] == target_label
    
    def evaluate_model(self):
        # k = 500
        test_cases = load_test_cases(self.dataset_name)

        counter = 0
        for test_case in tqdm(test_cases, desc="process"):
            flag = self.predict(test_case['text'], test_case['label'])
            if flag:
                counter += 1

        print("accuracy:", counter / len(test_cases))

def main():
    model_path = 'model/roberta-gyafc/checkpoint-3268'
    dataset_name = 'gyafc'

    classifier = Classifier(dataset_name, model_path)
    classifier.evaluate_model()

def test_model():
    test_cases = [
        ("the $ _num_ minimum charge to use a credit card is also annoying .", 0),
        ("sorry but i do n't get the rave reviews for this place .", 0),
        ("the desserts were very bland .", 0),
        ("the cake portion was extremely light and a bit dry .", 0),
        ("it was super dry and had a weird taste to the entire slice .", 0),
        ("excellent chinese and superb service .", 1),
        ("my favorite chinese food in az !", 1),
        ("it 's full of fresh ingredients , light and tasty .", 1),
        ("we had the shrimp with vegetables and shrimp fried rice - both lovely .", 1),
        ("they 're quite generous with the shrimp !", 1),
    ]

    counter = 0
    for test_case in test_cases:
        flag = Classifier.evaluate(test_case[0], test_case[1])
        if flag:
            counter += 1
    
    print("accuracy:", counter / len(test_cases))

def evaluate_batch(sentences: List[str]):
    dataset_name = 'yelp'

    classifier = Classifier(dataset_name)

    results = []
    for sentence in sentences:
        results.append(classifier.predict(sentence['1'], 1))

    # calculate the accuracy using counter
    counter = Counter(results)
    return counter.most_common(1)[0][1] / counter.total()

if __name__ == '__main__':
    main()