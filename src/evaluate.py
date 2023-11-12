import sys
sys.path.append('.')

import fire
import pandas as pd
from tqdm import tqdm

from utils.evaluate import EvalD
from utils.log import ScheduleLog
from utils.file import read_json, write_json
from bot import Bot

SYSTEM_PROMPT =  "There are some intructions below. You need to give the answer without any explation. If you are not asked to answer discretely, please round it to 3 decimal places"

class EvalConfig:
    def __init__(self, k: int, style_type: str, style1: str, 
            sentences_path: str, prompt_template_path: str,
            output_path: str):
        self.k = k
        self.style_type = style_type
        self.style1 = style1
        self.sentences_path = sentences_path
        self.prompt_template_path = prompt_template_path
        self.output_path = output_path

    @staticmethod
    def from_file(file_path: str):
        info = read_json(file_path)

        return EvalConfig(
            info['k'],
            info['style_type'],
            info['style1'],
            info['sentences_path'],
            info['prompt_template_path'],
            info['output_path']
        )

def generate_prompt(input: str, transferred: str, prompt_template: str,
        style_type: str, style1: str):
    prompt = prompt_template
    prompt = prompt.replace(f"{{input}}", input)
    prompt = prompt.replace(f"{{transferred}}", transferred)
    prompt = prompt.replace(f"{{style_type}}", style_type)
    prompt = prompt.replace(f"{{style1}}", style1)

    return prompt

# ='output/7b_chat_yelp/test.0.json'

def evaluate(eval_config_path: str):

    s_log = ScheduleLog(True)

    eval_config = EvalConfig.from_file(eval_config_path)

    all_prompt_templates = read_json(eval_config.prompt_template_path)
    sentences = read_json(eval_config.sentences_path)[:eval_config.k]
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
                prompt_templates = all_prompt_templates[eval_type]

                # 使用多个评价Prompt进行评分
                for prompt_template in tqdm(prompt_templates, desc="Prompts", position=2, leave=None):
                    # 生成多个prompt
                    prompt = generate_prompt(sentence['0'], sentence['1'], prompt_template, 
                        eval_config.style_type, eval_config.style1)
                    
                    while True:
                        try:
                            answer = Bot.ask(SYSTEM_PROMPT, prompt)
                            break
                        except:
                            # 当粗线错误时 重新调用
                            pass

                    result['score'][eval_type].append(answer)

            results.append(result)
            
        s_log.log("Evaluate Over!")
    except Exception as e:
        raise e
    finally:
        # 保存
        write_json(eval_config.output_path, results)
        s_log.log("Save Over!")


# 评测结果 评测时不输出输出结果
def evaluate_without_input(eval_config: EvalConfig):
    s_log = ScheduleLog(True)

    # 读取数据
    all_prompt_templates = read_json(eval_config.prompt_template_path)
    sentences = read_json(eval_config.sentences_path)[:eval_config.k]
    s_log.log("Load Over! (size={})".format(len(sentences)))

    results = []
    try:
        # 对每个句子进行评测
        for (i, sentence) in tqdm(enumerate(sentences), desc="Total Process", position=0):
            # 从3个评价唯独进行评分
            for eval_type in tqdm(EvalD, desc="Eval Dimension", position=1, leave=None):
                prompt_templates = all_prompt_templates[eval_type.value]

                # 使用多个评价Prompt进行评分
                for prompt_template in tqdm(prompt_templates, desc="Prompts", position=2, leave=None):
                    # 生成多个prompt
                    prompt = generate_prompt(sentence['0'], sentence['1'], prompt_template, 
                        eval_config.style_type, eval_config.style1)
                    
                    while True:
                        try:
                            answer = float(Bot.ask(SYSTEM_PROMPT, prompt))
                            break
                        # return -1 when meet transfer error
                        # if return None, it will be difficult to handle it later
                        except ValueError:
                            answer = -1; break
                        # 当出现超时错误时 重新调用
                        except: pass
                    
                    results.append([i, eval_type.value, answer])
            
        s_log.log("Evaluate Over!")
    except Exception as e:
        raise e
    finally:
        # 使用pandas转成csv保存
        df = pd.DataFrame(results, columns=['id', 'eval_d', 'score'])
        df.to_csv(eval_config.output_path, index=None)
        s_log.log("Save Over!")



def main(eval_config_path: str):
    eval_config = EvalConfig.from_file(eval_config_path)
    evaluate_without_input(eval_config)


if __name__ == '__main__':
    fire.Fire(main)
            