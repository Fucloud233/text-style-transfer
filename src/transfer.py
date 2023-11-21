import sys
sys.path.append(".")

import random 
import fire

from tqdm import tqdm

from typing import List

from utils.config import TransferConfig, LoadType, RetrievalType
from utils.file import write_json, read_lines, join_path, get_folder
from utils.log import ScheduleLog
from model.llama2 import Llama2, LlamaType
from model.llama2_enhance import Llama2withBM25, Llama2WithRandom

PROMPT = "There is a sentence '{}'. You should rewrite it more positive. The more positive sentence is {{"

END_SYMBOL = '}'

OUTPUT_FILENAME = 'transfer.json'

def load_dataset(dataset_path: str, k: int=-1, is_random: bool=True):
    lines = read_lines(dataset_path)
    
    if k == -1:
        return lines
    elif is_random:
        return random.sample(lines, k)
    else:
        return lines[:k]

def select_bot(
        prompt: str,
        retrieval_type: RetrievalType, 
        retrieval_path: str=""
    ):

    if retrieval_type == RetrievalType.Null:
        return Llama2(prompt)
    
    retrieval_dataset = load_dataset(retrieval_path)
    match retrieval_type:
        case RetrievalType.BM25:
            return Llama2withBM25(prompt, retrieval_dataset)
        case RetrievalType.Random:
            return Llama2WithRandom(prompt, retrieval_dataset)
        case _:
            print("The type of retrieval is invalid!")
            return          

def transfer(bot: Llama2, sentence: str) -> (str, str):
    # 从迁移结果中提取出有用的具体
    (result, prompt) = bot.transfer(sentence)
    # [注意] 还需要根据换行符换行 避免特殊情况
    result = result.split(END_SYMBOL)[0].split('\n')[0]

    return {
        "result": result,
        "prompt": prompt
    }

def run(config_path: str):
    config = TransferConfig(config_path)
    
    if config.k == "":
        print("The size of dataset to transfer no set!")
        return 
    
    # select the bot based on the type
    bot = select_bot(config.prompt, config.retrieval_type, config.retrieval_path)

    # load test dataset
    dataset = load_dataset(config.dataset_path, config.k, config.load_type)

    # transfer sentence 
    result = []
    for sentence in tqdm(dataset, desc="Dataset: "):
        output = transfer(bot, sentence)

        result.append({
            "0": sentence,
            "1": output['result'],
            "prompt": output['prompt']
        })
        
    # generate output path and save them
    output_path = join_path(get_folder(config_path), OUTPUT_FILENAME)
    write_json(output_path, result)

    print("Transfer Over!")

def run_batch(
    retrieval_types: List[RetrievalType],
    dataset_path: str,
    output_path: str,
    retrieval_path: str,
    k: int = -1
):  
    ordinal_prompt = "Here is a sentence {{ {sentence} }}. You should rewrite it more positive. The more positive sentence is {{"
    retrieval_prompt = "Here is a positive sentence: {{ {similar} }}.\nHere is a sentence {{ {sentence} }}. You should rewrite it more positive. The more positive sentence is {{"

    dataset = load_dataset(dataset_path, k)

    for retrieval_type in tqdm(retrieval_types, desc="Batch Process"):
        prompt = ordinal_prompt if retrieval_type == RetrievalType.Null \
            else retrieval_prompt
        
        bot = select_bot(prompt, retrieval_type, retrieval_path)

        result = []
        for sentence in tqdm(dataset, desc="Sentence Process", leave=None):
            output = transfer(bot, sentence)

            result.append({
                "0": sentence,
                "1": output['result'],
                "prompt": output['prompt']
            })

        cur_output_path = join_path(output_path, [retrieval_type.value, OUTPUT_FILENAME])
        write_json(cur_output_path, result)

        # print("{} transfer over!".format(retrieval_type.value))

def talk():
    bot = Llama2(PROMPT, LlamaType.Llama_7B_Chat)

    while True:
        print('='*50)
        sentence = input("You: ")
        if sentence == "exit": 
            break
        result = bot.transfer(sentence)
        print("bot:", result)

def main():
    retrieval_types = [RetrievalType.Null, RetrievalType.Random, RetrievalType.BM25]
    dataset_path = 'output/sentiment.test.0.1500'
    retrieval_path = 'data/yelp/sentiment.train.1'
    output_path = 'output/7b_1500'

    run_batch(retrieval_types, dataset_path, output_path, retrieval_path)
    
if __name__ == '__main__':
    # fire.Fire(run)
    # fire.Fire(transfer_7b_chat_yelp)

    main()