import sys
sys.path.append('.')

from typing import List

from src.model.kenlm_model import KenlmModel
from utils.file import read_json

def get_model() -> KenlmModel:
    return KenlmModel.from_pretrained("wikipedia", "en")

model = get_model()

def evaluate(sentence: str):
    return model.get_perplexity(sentence)


def evaluate_batch(sentences: List[str]):
    model = get_model()

    total = len(sentences)
    ppl_sum = 0
    for sentence in sentences:
        ppl_sum += model.get_perplexity(sentence['1'])
    
    return ppl_sum / total

# if __name__ == '__main__':
#     model = KenlmModel.from_pretrained("wikipedia", "en")
#     print(model.get_perplexity("I am very perplexed"))
#     print(model.get_perplexity("im perplexed trippin"))

