import sys
sys.path.append('.')

from typing import List
from tqdm import tqdm

from utils.config import RetrievalType
from utils.file import write_json, read_json, join_path
from utils.evaluate import EvalMetric, harmonic_mean, geometric_mean

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
    
    def evaluate(self, output_folder: str, filename: str=EVALUATE_OUTPUT_FILE, k: int=-1):
        evaluate_metrics = [EvalMetric.Style, EvalMetric.Content, EvalMetric.Fluency]
        mean_types = [EvalMetric.GM, EvalMetric.HM]

        evaluate_results = {}
        for result in tqdm(self.results_path, desc='Process'):
            sentences = read_json(result['path'])
            sentences = sentences if k == -1 else sentences[:k]

            results = {}
            for metric in evaluate_metrics:
                results[metric] = self.__evaluate_single(sentences, metric)
            
            data_arr = [results[mean_type] for mean_type in mean_types]
            for mean_type in mean_types:
                results[mean_type] = self.__mean_result(data_arr, mean_type)

            evaluate_results[result['retrieval']] = result

        output_path = join_path(output_folder, filename)
        write_json(output_path, evaluate_results)

        print("Evaluate Over!")

    def __evaluate_single(self, sentences: List[str], metric: EvalMetric, precision: int=2) -> str:
        match metric:
            case EvalMetric.Style: score = roberta_batch_eval(sentences)
            case EvalMetric.Content: score = sacre_bleu_batch_eval(sentences)
            case EvalMetric.Fluency: score = ppl_batch_eval(sentences)

        return round(score, precision)
    
    def __mean_result(self, results: List[str], metric: EvalMetric, precision: int=2):
        match metric:
            case EvalMetric.GM: score = geometric_mean(results)
            case EvalMetric.HM: score = harmonic_mean(results)

        return round(score, precision)

def mean_evaluate_result():
    dataset_names = ['yelp', 'gyafc']

    for dataset_name in tqdm(dataset_names, desc='Dataset'):
        results_path = 'output/7b_{}_0_1500'.format(dataset_name)
        output_path = join_path(results_path, ['evaluate', EVALUATE_OUTPUT_FILE])

        result: dict = read_json(output_path)
        for (key, value) in result.items():
            style = value['style'] * 100
            content = value['bleu']

            score_list = [style, content]

            result[key]["HM"] = harmonic_mean(score_list)
            result[key]["GM"] = geometric_mean(score_list)

        write_json(output_path, result)


def main_retrieval():
    kinds = [RetrievalType.Null, RetrievalType.BM25, RetrievalType.Random, RetrievalType.GTR]
    dataset_names = ['yelp', 'gyafc']

    for dataset_name in tqdm(dataset_names, desc='Dataset'):
        results_path = 'output/7b_{}_0_1500'.format(dataset_name)
        output_path = join_path(results_path, 'evaluate')
        filename = 'test.json'
        k = 5
    
        # evaluate ...
        evaluator = Evaluator()
        evaluator.append_retrieval_results(kinds, results_path)
        evaluator.evaluate(output_path, filename, k)    

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
    # main_retrieval()
    mean_evaluate_result()