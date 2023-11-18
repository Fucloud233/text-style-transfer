import sys
sys.path.append(".")

from tqdm import tqdm
from transformers import pipeline
from transformers import RobertaTokenizer

from utils.file import read_yelp_test_cases


MODEL_PATH = "model/roberta/"
REPOSITORY_ID = 'roberta-large'

class Classifier:
    tokenizer = RobertaTokenizer.from_pretrained(REPOSITORY_ID)

    classifier = pipeline(
        task="sentiment-analysis",
        model=MODEL_PATH,
        tokenizer=tokenizer,
        device='cpu')

    @staticmethod
    def evaluate(sentence: str, style_id: int) -> bool:
        result = Classifier.classifier(sentence)
        target_label = 'LABEL_{}'.format(style_id)
        return result[0]['label'] == target_label

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


def test_total_model():
    k = 500
    test_cases = read_yelp_test_cases(k=k)
    
    counter = 0
    for test_case in tqdm(test_cases, desc="process"):
        flag = Classifier.evaluate(test_case['text'], test_case['label'])
        if flag:
            counter += 1

    print("accuracy:", counter / len(test_cases))


if __name__ == '__main__':
    test_total_model()