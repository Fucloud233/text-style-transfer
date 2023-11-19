import sys
sys.path.append('.')

# it will append current module path by default
# sys.path.append('./src')

from utils.config import RetrievalType
from utils.file import write_json, read_json

def runner(results, output_path):
    from roberta import evaluate_batch as style_eval
    from sacre_bleu import evaluate_batch as bleu_eval
    from ppl import evaluate_batch as ppl_eval

    fastText_model_path = 'model/fastText.bin'
    target_style = 'positive'

    evaluate_result = {}
    for result in results:
        # model_path = 'model/fastText.bin'
        # target_style = 'positive'
        # evaluate_result[result['retrieval'].value] =  accuracy(model_path, result['path'], target_style)

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
        sentences = read_json(result['path'])

        evaluate_result[result['retrieval'].value] = {
            # "style": style_eval(sentences, fastText_model_path, target_style),
            "style": style_eval(sentences, target_style),
            "bleu": bleu_eval(sentences),
            "ppl": ppl_eval(sentences)
        }
    
    write_json(output_path, evaluate_result)

    print("Transfer Over!")

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

def main():
    
    results = [{
            "path": 'output/7b_0_100/transfer.json',
            "retrieval": RetrievalType.Null,
        },{
            "path": 'output/7b_0_100/bm25/transfer.json',
            "retrieval": RetrievalType.BM25,
        }
    ]

    output = 'output/7b_0_100/evaluate/'

    runner(results, output + 'result.json')
    # runner_debug(results, output + 'result_debug.json')

if __name__ == '__main__':
    main()