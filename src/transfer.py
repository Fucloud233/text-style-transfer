import sys
sys.path.append(".")

import json
import random 
import fire

from tqdm import tqdm

from utils.config import TransferConfig, LoadType, RetrievalType
from utils.file import write_json
from utils.log import ScheduleLog
from model.llama2 import Llama2, LlamaType

PROMPT = "There is a sentence '{}'. You should rewrite it more positive. The more positive sentence is {{"

END_SYMBOL = '}'

def load_dataset(dataset_path: str, k: int, load_type: LoadType=LoadType.Front):
    datasets = []
    
    # read dataset in batches
    for path in dataset_path:
        with open(path, 'r', encoding='utf-8') as f:
            # 选择前k条
            if(load_type == LoadType.Front):
                dataset = [f.readline().strip() for _ in range(k)]
            # 随机选择
            elif(load_type == LoadType.Random):
                datas = f.read().splitlines()
                dataset = random.sample(datas, k)
            else:
                continue

        datasets.append(dataset)
    
    return datasets

def transfer_7b_chat_yelp(config: TransferConfig):
    if config.k == "":
        print("The size of dataset to transfer no set!")
        return 
    
    s_log = ScheduleLog(); s_log.start()
    s_log.log('Loading Dataset.')
    
    # load n pieces of data from multiple datasets
    datasets = load_dataset(config.dataset_path, config.k, config.load_type)    
    datasets_len = [len(dataset) for dataset in datasets]
    s_log.log(f'Load over. (size = {datasets_len}).')

    # 使用Llama转换
    retrieval_type = config.retrieval_type
    if(retrieval_type == RetrievalType.Null):
        bot = Llama2(PROMPT, LlamaType.Llama_7B_Chat) 
    elif(retrieval_type == RetrievalType.BM25):
        pass
    else:
        print("The type of retrieval is invalid!")
        return
            
    transfer_result = []
    for sentence in tqdm(datasets[config.select_index], desc="Dataset: "):
        # 从迁移结果中提取出有用的具体
        result = bot.transfer(sentence)
        # [注意] 还需要根据换行符换行 避免特殊情况
        result = result.split(END_SYMBOL)[0].split('\n')[0]
        transfer_result.append(result)
    s_log.log('Transfer over.')

    # 保存数据
    merge = [ {"0": i, "1": r} for (i, r) in zip(input, result) ]
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

def run(path: str):
    transfer_config = TransferConfig.from_file(path)
    transfer_7b_chat_yelp(transfer_config)
    
    
if __name__ == '__main__':
    fire.Fire(run)
    # fire.Fire(transfer_7b_chat_yelp)