import sys
sys.path.append('.')

from utils.file import read_json, write_json
from utils.config import RetrievalType

from nltk.translate.bleu_score import sentence_bleu

def evaluate(sentences_path: str, k: int):
    sentences = read_json(sentences_path)[: k]

    sum = 0
    for sentence in sentences:
        sum += sentence_bleu([sentence['0'].split()], sentence['1'].split())
    
    return sum / k * 100

def main():
    # sentences_path = 'output\\7b_0_100\\transfer.json'
    results = [{
            "path": 'output\\7b_0_100\\transfer.json',
            "retrieval": RetrievalType.Null,
            "k": 100
        },{
            "path": 'output\\7b_0_100\\bm25\\transfer.json',
            "retrieval": RetrievalType.BM25,
            "k": 100
        }
    ]

    evaluate_result = {}
    for result in results:
        evaluate_result[result['retrieval'].value] = evaluate(result['path'], result['k'])

    output_path = './output/7b_0_100/bleu/result.json'
    write_json(output_path, evaluate_result)
    

if __name__ == '__main__':
    main()