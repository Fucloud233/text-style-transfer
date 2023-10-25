import json
import random 
from enum import IntEnum

from utils import time
from utils.log import ScheduleLog
from llama2 import Llama2, LlamaType

PROMPT = "There is a sentence '{}'. You should rewrite it more positive. The more positive sentence is {{"\

class LoadType(IntEnum):
    Front = 0, 
    Random = 1,

def load_dataset(dataset_path: str, k: int, load_type: LoadType=LoadType.Front):
    with open(dataset_path, 'r', encoding='utf-8') as f:
        if(load_type == LoadType.Front):
            return f.readlines(k)
        elif(load_type == LoadType.Random):
            datas = f.readlines()
            return random.sample(datas, k)
        else:
            return None

def save_result(result: list, output_path: str):
    with open(output_path, 'w', encoding='utf-8') as f:
        # for sentence in result:
        #     f.write(f'"{sentence}"')
        f.write(json.dumps(result, indent=4))

def save_result_with_input(input: list, result: list, output_path: str):
    merge = [{"0": i, "1": r} for (i, r) in zip(input, result)]
    
    with open(output_path, 'w', encoding='utf-8') as f:
        # for sentence in result:
        #     f.write(f'"{sentence}"')
        f.write(json.dumps(merge, indent=4))

def transfer_7b_chat_yelp(k: int):
    dataset_path = 'data/yelp/sentiment.test.0'
    output_path = 'output/7b_chat_yelp/test.0.json'
    
    s_log = ScheduleLog(); s_log.start()
    s_log.log('Loading Dataset.')
    
    # 读取k条数据集
    dataset = load_dataset(dataset_path, k)    
    s_log.log(f'Load over: {len(dataset)}.')

    # 使用Llama转换
    bot = Llama2(PROMPT, LlamaType.Llama_7B_Chat) 
    transfer_result = []
    for sentence in dataset:
        transfer_result.append(bot.transfer(sentence))
    s_log.log('Transfer over.')

    # 保存数据
    # save_result(transfer_result, output_path)
    save_result_with_input(dataset, transfer_result, output_path)
    s_log.log('Save over.')

def main():
    bot = Llama2(PROMPT, LlamaType.Llama_7B_Chat)

    while True:
        print('='*50)
        sentence = input("You: ")
        if sentence == "exit": 
            break
        result = bot.transfer(sentence)
        print("bot:", result)


if __name__ == '__main__':
    transfer_7b_chat_yelp(10)