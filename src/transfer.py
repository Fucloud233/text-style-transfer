import sys; sys.path.append(".")

import random 
from tqdm import tqdm
from typing import List

from utils.config import TransferConfig, RetrievalType, BotType
from utils.file import write_json, read_lines, join_path, get_folder
from model.transfer_bot import TransferBot

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
        bot_kind: BotType,
        retrieval_type: RetrievalType, 
        dataset_name: str="",
        mix_rate: float=1
    ) -> TransferBot:

    kwargs = {}
    if bot_kind == BotType.Llama_7B:
        kwargs['api_url'] = 'http://127.0.0.1:5000/chat'

    if retrieval_type == RetrievalType.Null:
        return TransferBot(bot_kind, **kwargs)
    
    if retrieval_type in [RetrievalType.Random, RetrievalType.BM25, RetrievalType.MixBM25, RetrievalType.MixGTR]:
        retrieval_path = 'data/{}/train.1'.format(dataset_name)
        kwargs['retrieval_dataset'] = load_dataset(retrieval_path)
    
    if retrieval_type in [RetrievalType.MixBM25, RetrievalType.MixGTR]:
        kwargs['mix_rate'] = mix_rate

    if retrieval_type in [RetrievalType.GTR, RetrievalType.MixGTR]:
        kwargs['dataset_name'] = dataset_name

    return TransferBot(bot_kind, retrieval_type, **kwargs)


def transfer(
        bot: TransferBot, 
        sentence: str, 
        target_style: str, 
        retrieval_num: int=1
    ) -> (str, str):
    # don't need to pass retrieval_num to basic Llama2
    (result, prompt) = bot.transfer(sentence, target_style) if bot.retrieval_kind == RetrievalType.Null \
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

# ==================== PROMPT EDITING ====================

OrdinaryPrompt = "Here is a sentence {sentence}. You should rewrite it more {target}. The more {target} sentence is {{"
OneRetrievalPrompt = "Here is a {target} sentence: {similar} .\n" \
    "Here is a sentence {sentence}. You should rewrite it more {target} like the sentence above. The more {target} sentence is {{"
FewRetrievalPrompt = "Here are some {target} sentences: \n" \
    "{similar}\n" \
    "Here is a sentence {sentence}. You should rewrite it more {target} like the sentences above. The more {target} sentence is {{"

StyleMap = {
    "yelp": ["negative", "positive"],
    "gyafc": ["informal", "formal"]
}

def run_batch(
    bot_kind: BotType,
    dataset_name: str,
    k: int,
    retrieval_types: List[RetrievalType],
    retrieval_nums: List[int] = [1],
    dataset_path: str=None,
):  
    if dataset_path == None:
        dataset_path = 'output/{}.test.0.{}'.format(dataset_name, k)
    output_path = 'output/{}_{}_0_{}'.format(bot_kind.value, dataset_name, k)

    target_style = StyleMap[dataset_name][1]
    # handle with meeting single number input
    retrieval_nums = [retrieval_nums] if isinstance(retrieval_nums, int) else retrieval_nums
    
    dataset = load_dataset(dataset_path)[:k]

    # encapsulate logic function
    def runner_logic(prompt: str, retrieval_num: int=0):
        # 1. set the prompt
        bot.set_prompt(prompt)

        # 2. transfer sentences
        result = []
        for sentence in tqdm(dataset, desc="Sentence Process", leave=None):
            output = transfer(bot, sentence, target_style, retrieval_num)

            result.append({
                "0": sentence,
                "1": output['result'],
                "prompt": output['prompt']
            })

        # 3. generate output filename
        # output_filename = OUTPUT_FILENAME if retrieval_num == 1 \
        #     else str(retrieval_num) + '_' + OUTPUT_FILENAME\
        output_filename = str(retrieval_num) + '_' + OUTPUT_FILENAME

        # 4. save them into files
        cur_output_path = join_path(output_path, [retrieval_type.value, output_filename])
        write_json(cur_output_path, result)


    for retrieval_type in tqdm(retrieval_types, desc="Retrieval Type"):
        bot = select_bot(bot_kind, retrieval_type, dataset_name)

        if retrieval_type == RetrievalType.Null:
            runner_logic(OrdinaryPrompt)
            continue

        for retrieval_num in tqdm(retrieval_nums, desc="Retrieval Num", leave=None):
            prompt = OneRetrievalPrompt if retrieval_num == 1 \
                else FewRetrievalPrompt
            runner_logic(prompt, retrieval_num)

def run_rate(    
    bot_kind: BotType,
    dataset_name: str,
    k: int,
    mix_rates: List[float],
    retrieval_types: List[RetrievalType],
    retrieval_num: int = 10,
    dataset_path: str=None,
):  
    if dataset_path == None:
        dataset_path = 'output/{}.test.0.{}'.format(dataset_name, k)
    output_path = 'output/{}_{}_0_{}'.format(bot_kind.value, dataset_name, k)

    target_style = StyleMap[dataset_name][1]
    # handle with meeting single number input
    
    dataset = load_dataset(dataset_path)[:k]

    # encapsulate logic function
    def runner_logic(prompt: str, mix_rate: float):
        # 1. set the prompt
        bot.set_prompt(prompt)

        # 2. transfer sentences
        result = []
        for sentence in tqdm(dataset, desc="Sentence Process", leave=None):
            output = transfer(bot, sentence, target_style, retrieval_num)

            result.append({
                "0": sentence,
                "1": output['result'],
                "prompt": output['prompt']
            })

        # 3. generate output filename
        output_filename = str(retrieval_num) + '_' + str(int(mix_rate * 10)) + '_' + OUTPUT_FILENAME

        # 4. save them into files
        cur_output_path = join_path(output_path, [retrieval_type.value, output_filename])
        write_json(cur_output_path, result)

    for retrieval_type in tqdm(retrieval_types, desc="Retrieval Type"):
        for mix_rate in tqdm(mix_rates, desc="Mix Rate", leave=None):
            bot = select_bot(bot_kind, retrieval_type, dataset_name, mix_rate=mix_rate)
            prompt = FewRetrievalPrompt
            runner_logic(prompt, mix_rate)


def talk():
    prompt = "There is a sentence '{sentence}'. You should rewrite it more {target}. The more positive sentence is {{"

    bot = TransferBot()
    bot.set_prompt(prompt)

    while True:
        print('='*50)
        sentence = input("You: ")
        if sentence == "exit": 
            break
        result = bot.transfer(sentence, 'positive')
        print("bot:", result)

def main():
    retrieval_types = [
        RetrievalType.Null, 
        RetrievalType.Random, 
        RetrievalType.BM25,
        RetrievalType.GTR,
        RetrievalType.MixBM25,
        RetrievalType.MixGTR
    ]
    retrieval_num = [
        1, 
        2, 
        4, 
        8, 
        10
    ]

    bot_kind = BotType.Llama_7B
    dataset_name = 'gyafc'
    num = 1500
    test_dataset_name = 'output/{}.test.0.1500'.format(dataset_name)

    run_batch(
        bot_kind, 
        dataset_name, 
        num, 
        retrieval_types, 
        retrieval_num, 
        test_dataset_name
    )

def main_rate():
    retrieval_types= [RetrievalType.BM25, RetrievalType.GTR]

    mix_rates = [
        0.1, 0.2, 0.4, 0.6, 0.8
    ]

    bot_kind = BotType.Llama_7B
    dataset_name = 'gyafc'
    num = 1500
    test_dataset_name = 'output/{}.test.0.1500'.format(dataset_name)

    run_rate(
        bot_kind, 
        dataset_name, 
        num, 
        mix_rates,
        retrieval_types,
        10,
        test_dataset_name
    )
    
if __name__ == '__main__':
    # talk()

    main_rate()