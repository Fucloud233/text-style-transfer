import sys; sys.path.append('.')

import numpy as np
import matplotlib
from matplotlib import pyplot as plt
from utils.file import read_json
from utils.config import RetrievalType
from utils.evaluate import EvalMetric

matplotlib.rcParams.update({'font.size': 12}) 

def draw(model_name: str, dataset_name: str, k: int, need_show: bool=True):
    output_path = "output/{}_{}_0_{}/evaluate/".format(model_name, dataset_name, k)

    # read evaluation from files
    eval_result_path = output_path + 'evaluate.json'
    eval_result = read_json(eval_result_path)

    eval_metrics = [metric.value for metric in EvalMetric]
    retrieval_kinds = [kind.value for kind in RetrievalType]

    # init a dict for recording 
    draw_result = {}
    for metric in eval_metrics:
        draw_result[metric] = {}

    # convert evaluation result for drawing
    retrieval_num = []
    for metric in eval_metrics:
        for kind in retrieval_kinds:
            if kind == 'null':
                draw_result[metric][kind] = eval_result[kind][metric]
            else:
                results = eval_result[kind]
                retrieval_num = [str(num) for num in sorted([int(key) for key in results.keys()])]
                draw_result[metric][kind] = [results[num][metric] for num in retrieval_num]

    colors = {
        'random': 'r', 
        'bm25': 'g', 
        'gtr': 'b'
    }

    plt.figure(figsize=(15, 18))

    kinds_num = len(retrieval_kinds) - 1
    w = 1 / kinds_num - 0.1
    for (i, (metric, eval_result)) in enumerate(draw_result.items()):
        plt.subplot(len(draw_result), 1, i+1)
        plt.title(metric)

        for (j, kind) in enumerate(colors.keys()):
            plt.bar(
                np.arange(len(retrieval_num)) + j*w, 
                eval_result[kind], 
                w, 
                color=colors[kind],
                label=kind
            )

        plt.axhline(eval_result['null'], linestyle='--', label='base')
        plt.xticks(np.arange(len(retrieval_num)), retrieval_num)
        
        # add notaion 
        plt.legend(loc='lower right')
    
    # total title
    plt.suptitle(dataset_name + ' dataset', fontsize=24)

    # save to file
    save_path = eval_result_path = output_path + 'diagram.png'
    plt.savefig(save_path)

    # show
    if need_show:
        plt.show()

def main():
    model_name = 'gpt'
    dataset_name = "yelp"
    k = 1500
    draw(model_name, dataset_name, k)

if __name__ == '__main__':
    main()
