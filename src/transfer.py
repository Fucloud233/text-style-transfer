import sys
sys.path.append(".")

import json
import random 
import fire

from tqdm import tqdm
from typing import List

from utils.config import TransferConfig, LoadType, RetrievalType
from utils.file import write_json
from utils.log import ScheduleLog
from model.llama2 import Llama2, LlamaType
from model.llama2_bm25 import Llama2withBM25

PROMPT = "There is a sentence '{}'. You should rewrite it more positive. The more positive sentence is {{"

END_SYMBOL = '}'

def load_dataset(dataset_path: str, k: int=-1, load_type: LoadType=LoadType.Front):
    with open(dataset_path, 'r', encoding='utf-8') as f:
        # 选择前k条
        if(load_type == LoadType.Front):
            if k == -1:
                return f.read(-1).splitlines()

            return [f.readline().strip() for _ in range(k)]
        # 随机选择
        elif(load_type == LoadType.Random):
            datas = f.read().splitlines()
            return random.sample(datas, k)
        else:
            return None

def select_bot(prompt: str, llama_type: LlamaType, 
        retrieval_type: RetrievalType, 
        retrieval_path: str=""
    ):

    if(retrieval_type == RetrievalType.Null):
        return Llama2(prompt, llama_type) 
    elif(retrieval_type == RetrievalType.BM25):
        retrieval_dataset = load_dataset(retrieval_path)
        return Llama2withBM25(prompt, retrieval_dataset, llama_type)
    else:
        print("The type of retrieval is invalid!")
        return

def transfer(bot: Llama2, sentence: str) -> (str, str):
    # 从迁移结果中提取出有用的具体
    (result, prompt) = bot.transfer(sentence)
    # [注意] 还需要根据换行符换行 避免特殊情况
    result = result.split(END_SYMBOL)[0].split('\n')[0]

    return (result, prompt)

def run(path: str):
    config = TransferConfig(path)
    
    if config.k == "":
        print("The size of dataset to transfer no set!")
        return 
    
    s_log = ScheduleLog(); s_log.start()

    # select the bot based on the type
    bot = select_bot(config.prompt, config.llama_type, config.retrieval_type, config.retrieval_path)

    # load test dataset
    dataset = load_dataset(config.dataset_path, config.k, config.load_type)
    s_log.log('Load over. ({})'.format(len(dataset)))

    # transfer sentence 
    result = []
    for sentence in tqdm(dataset, desc="Dataset: "):
        result.append(transfer(bot, sentence)) 
    s_log.log('Transfer over.')

    # save them
    merge = [ {"0": i, "1": r} for (i, r) in zip(dataset, result) ]
    write_json(config.output_path, merge)
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
    fire.Fire(run)
    # fire.Fire(transfer_7b_chat_yelp)