import sys
sys.path.append('.')

from typing import List
from tqdm import tqdm

from utils.config import RetrievalType
from utils.file import write_json, read_json, join_path

from roberta import evaluate_batch as roberta_batch_eval
from sacre_bleu import evaluate_batch as sacre_bleu_batch_eval
from ppl import evaluate_batch as ppl_batch_eval

def runner_debug(results, output_path):
    from fast_text import evaluate as style_eval
    from sacre_bleu import evaluate as bleu_eval
    from ppl import evaluate as ppl_eval

    all_sentences = [read_json(result['path']) for result in results]

    total = len(all_sentences[0])

    eval_result = []

    # each sentences
    for i in range(total):
        src_sentence = all_sentences[0][i]['0']
        tmp_eval_result ={ 
            '0': src_sentence,
            'results': [] 
        }

        for (result, sentences) in zip(results, all_sentences):
            tgt_sentence = sentences[i]['1']
            prompt = sentences[i]['prompt']

            tmp_eval_result['results'].append({
                "1": tgt_sentence,
                'retrieval': result['retrieval'].value,
                "prompt": prompt,
                "style": style_eval(tgt_sentence),
                "bleu": bleu_eval(src_sentence, tgt_sentence),
                "ppl": ppl_eval(tgt_sentence)
            })
        
        # check the evaluate result same
        first_style = tmp_eval_result['results'][0]['style']
        flag = False
        for result in tmp_eval_result['results'][1:]:
            if first_style != result['style']:
                # print(first_style, result['style'])
                flag = True
                break

        if flag:
            eval_result.append(tmp_eval_result)


    write_json(output_path, eval_result)

'''
sentences type
[
    {
        "0": "source_sentence",
        "1": "target_sentence",
        "prompt": "prompt"
    }
]
'''

TRANSFER_OUTPUT_FILE = 'transfer.json'
EVALUATE_OUTPUT_FILE = 'evaluate.json'

class Evaluator:
    def __init__(self):
        self.results_path = []

    def append_results(self, names: List[str], output: str, filename: str=TRANSFER_OUTPUT_FILE):
        for name in names:
            self.results_path.append({
                "path": join_path(output, [name, filename]),
                "retrieval": name,
            })
        
    def append_retrieval_results(self, kinds: List[RetrievalType], output: str):
        kinds_str = [kind.value for kind in kinds]
        self.append_results(kinds_str, output)
    
    def evaluate(self, output_folder: str, filename: str=EVALUATE_OUTPUT_FILE):
        evaluate_result = {}
        for result in tqdm(self.results_path, desc='Process'):
            sentences = read_json(result['path'])

            evaluate_result[result['retrieval']] = {
                "style": roberta_batch_eval(sentences),
                "bleu": sacre_bleu_batch_eval(sentences),
                "ppl": ppl_batch_eval(sentences)
            }  

        output_path = join_path(output_folder, filename)
        write_json(output_path, evaluate_result)

        print("Evaluate Over!")


def main_retrieval():
    kinds = [RetrievalType.Null, RetrievalType.BM25, RetrievalType.Random, RetrievalType.GTR]
    dataset_names = ['yelp', 'gyafc']

    for dataset_name in tqdm(dataset_names, desc='Dataset'):
        results_path = 'output/7b_{}_0_1500'.format(dataset_name)
        output_path = join_path(results_path, 'evaluate')
        filename = 'evaluate.json'
    
        # evaluate ...
        evaluator = Evaluator()
        evaluator.append_retrieval_results(kinds, results_path)
        evaluator.evaluate(output_path, filename)    

def main():
    names = []
    results_path = 'output/traditional'
    output_path = join_path(results_path, 'evaluate')

    evaluator = Evaluator()
    evaluator.append_results(
        names, 
        results_path, 
        filename=TRANSFER_OUTPUT_FILE
    )
    evaluator.evaluate(
        output_path,
        filename=EVALUATE_OUTPUT_FILE
    )

if __name__ == '__main__':
    main_retrieval()