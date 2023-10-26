import sys
sys.path.append('.')

import fire
from tqdm import tqdm

from utils.log import ScheduleLog
from utils.file import read_json, write_json
from bot import Bot

SYSTEM_PROMPT =  "There are some intructions below. You need to give the answer without any explation. If you are not asked to answer discretely, please round it to 3 decimal places"

def generate_prompt(input: str, transferred: str, prompt_template=str):
    prompt = prompt_template
    prompt = prompt.replace(f"{{input}}", input)
    prompt = prompt.replace(f"{{transferred}}", transferred)

    return prompt

def evaluate(k: int):
    prompt_tempalates_path = 'data/eval_prompts.json'
    sentences_path = 'output/7b_chat_yelp/test.0.json'

    s_log = ScheduleLog(True)

    all_prompt_tempalates = read_json(prompt_tempalates_path)
    sentences = read_json(sentences_path)[:k]
    s_log.log("Load Over! (size={})".format(len(sentences)))

    
    # 对翻译的具体进行评分
    results = []

    try:
        for sentence in tqdm(sentences, desc="Total Process", position=0):
            result = {
                "0": sentence["0"],
                "1": sentence["1"],
                "score": {
                    'style': [],
                    'content': [],
                    'fluency': []
                }
            }
            
            # 从3个评价唯独进行评分
            for eval_type in tqdm(result['score'].keys(), desc="Eval Dimension", position=1, leave=None):
                prompt_templates = all_prompt_tempalates[eval_type]

                # 使用多个评价Prompt进行评分
                for prompt_template in tqdm(prompt_templates, desc="Prompts", position=2, leave=None):
                    prompt = generate_prompt(sentence['0'], sentence['1'], prompt_template)
                    answer = Bot.ask(SYSTEM_PROMPT, prompt)

                    result['score'][eval_type].append(answer)

            results.append(result)
            
            s_log.log("Evaluate Over!")
    except Exception as e:
        raise e
    finally:
        # 保存
        write_json('output/7b_chat_yelp/eval_result.raw.json', results)
        s_log.log("Save Over!")

def main():
    fire.Fire(evaluate)

if __name__ == '__main__':
    main()
            