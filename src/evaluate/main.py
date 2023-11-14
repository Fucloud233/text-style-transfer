import sys
sys.path.append('.')
sys.path.append('./src')

from utils.config import RetrievalType
from utils.file import write_json, read_json

from evaluate.fastText import evaluate as style_eval
from evaluate.bleu import evaluate as bleu_eval
from evaluate.ppl import evaluate as ppl_eval

def runner(results, output_path):
    fastText_model_path = 'model/fastText.bin'
    target_style = 'positive'

    evaluate_result = {}
    for result in results:
        # model_path = 'model/fastText.bin'
        # target_style = 'positive'
        # evaluate_result[result['retrieval'].value] =  accuracy(model_path, result['path'], target_style)

        sentences = read_json(result['path'])

        evaluate_result[result['retrieval'].value] = {
            "style": style_eval(sentences, fastText_model_path, target_style),
            "bleu": bleu_eval(sentences),
            "ppl": ppl_eval(sentences)
        }
    
    write_json(output_path, evaluate_result)

def main():
    
    results = [{
            "path": 'output/7b_0_100/transfer.json',
            "retrieval": RetrievalType.Null,
        },{
            "path": 'output/7b_0_100/bm25/transfer.json',
            "retrieval": RetrievalType.BM25,
        }
    ]

    runner(results, 'output/7b_0_100/evaluate/result.json')

if __name__ == '__main__':
    main()