import sys
sys.path.append(".")

import random 
from tqdm import tqdm
from typing import List

from utils.config import TransferConfig, RetrievalType
from utils.file import write_json, read_lines, join_path, get_folder
from model.llama2 import Llama2
from model.llama2_enhance import Llama2withBM25, Llama2WithRandom, Llama2withGTR

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
        retrieval_type: RetrievalType, 
        dataset_name: str=""
    ):

    if retrieval_type == RetrievalType.Null:
        return Llama2()
    
    retrieval_path = 'data/{}/train.1'.format(dataset_name)
    match retrieval_type:
        case RetrievalType.Random:
            return Llama2WithRandom(load_dataset(retrieval_path))
        case RetrievalType.BM25:
            return Llama2withBM25(load_dataset(retrieval_path))
        case RetrievalType.GTR:
            return Llama2withGTR(dataset_name)
        case _:
            raise ValueError("The type of retrieval is invalid!")

def transfer(bot: Llama2, sentence: str, target_style: str, retrieval_num: int=1) -> (str, str):
    # don't need to pass retrieval_num to basic Llama2
    (result, prompt) = bot.transfer(sentence, target_style) if bot.type == RetrievalType.Null \
        else bot.transfer(sentence, target_style, retrieval_num)

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

OrdinaryPrompt = "Here is a sentence {sentence}. You should rewrite it more {target}. The more {target} sentence is {{"
OneRetrievalPrompt = "Here is a {target} sentence: {similar} .\n" \
    "Here is a sentence {sentence}. You should rewrite it more {target}. The more {target} sentence is {{"
FewRetrievalPrompt = "Here are some {target} sentences: \n" \
    "{similar}\n" \
    "Here is a sentence {sentence}. You should rewrite it more {target}. The more {target} sentence is {{"

StyleMap = {
    "yelp": ["negative", "positive"],
    "gyafc": ["informal", "formal"]
}


def run_batch(
    dataset_name: str,
    k: int,
    retrieval_types: List[RetrievalType],
    retrieval_nums: List[int] = [1],
    dataset_path: str=None,
    save_to_path: bool=False
):  
    if dataset_path == None:
        dataset_path = 'output/{}.test.0.{}'.format(dataset_name, k)
    output_path = 'output/7b_{}_0_{}'.format(dataset_name, k)

    target_style = StyleMap[dataset_name][1]
    # handle with meeting single number input
    retrieval_nums = [retrieval_nums] if isinstance(retrieval_nums, int) else retrieval_nums
    
    dataset = load_dataset(dataset_path)[:k]

    # encapsulate logic function
    def runner_logic(prompt: str, retrieval_num: int=1):
        # 1. set the prompt
        bot.set_prompt(prompt)

        # 2. transfer sentences
        result = []
        for sentence in dataset if save_to_path else tqdm(dataset, desc="Sentence Process", leave=None):
            output = transfer(bot, sentence, target_style, retrieval_num)

            result.append({
                "0": sentence,
                "1": output['result'],
                "prompt": output['prompt']
            })

        # 3. generate output filename
        output_filename = OUTPUT_FILENAME if retrieval_num == 1 \
            else str(retrieval_num) + '_' + OUTPUT_FILENAME

        # 4. save them into files
        cur_output_path = join_path(output_path, [retrieval_type.value, output_filename])
        write_json(cur_output_path, result)


    for retrieval_type in tqdm(retrieval_types, desc="Retrieval Type"):
        bot: Llama2 = select_bot(retrieval_type, dataset_name)

        if retrieval_type == RetrievalType.Null:
            runner_logic(OrdinaryPrompt)
            continue

        for retrieval_num in tqdm(retrieval_nums, desc="Retrieval Num", leave=None):
            prompt = OneRetrievalPrompt if retrieval_num == 1 \
                else FewRetrievalPrompt
            runner_logic(prompt, retrieval_num)

def talk():
    prompt = "There is a sentence '{}'. You should rewrite it more positive. The more positive sentence is {{"

    bot = Llama2()
    bot.set_prompt(prompt)

    while True:
        print('='*50)
        sentence = input("You: ")
        if sentence == "exit": 
            break
        result = bot.transfer(sentence)
        print("bot:", result)

def main():
    retrieval_types = [
        RetrievalType.Null, 
        RetrievalType.Random, 
        RetrievalType.BM25,
        RetrievalType.GTR
    ]
    retrieval_num = [1, 2, 4, 8, 10]
    # retrieval_num = [1]

    dataset_name = 'gyafc'
    num = 1500

    test_dataset_name = 'output/gyafc.test.0.1500'

    run_batch(dataset_name, num, retrieval_types, retrieval_num, test_dataset_name, True)
    
if __name__ == '__main__':
    # fire.Fire(run)
    # fire.Fire(transfer_7b_chat_yelp)

    main()