import sys
sys.path.append('.')

from nltk.translate.bleu_score import sentence_bleu

def evaluate(src: str, tgt: str):
    return sentence_bleu([src.split()], tgt.split()) * 100

def evaluate_batch(sentences: str):
    total = len(sentences)
    sum = 0
    for sentence in sentences:
        sum += sentence_bleu([sentence['0'].split()], sentence['1'].split())
    
    return sum / total * 100