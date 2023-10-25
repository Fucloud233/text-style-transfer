from llama import Llama
from typing import List

MAX_BATCH_SIZE = 4

MAX_GEN_LEN: int = 64
TEMPERATURE = 0.5
TOP_P = 0.9

PROMPT_PATH = 'data/prompts.txt'

def read_prompt():
    with open(PROMPT_PATH, 'r', encoding='utf-8') as f:
        prompt = f.readline().strip()
    
    return prompt

def main():
    generator = Llama.build(
        ckpt_dir="model/llama-2-7b-chat/",
        tokenizer_path="model/tokenizer.model",
        max_seq_len=256,
        max_batch_size=4
    )

    while True:
        sentence = input("Your: ")
        if sentence == 'exit':
            break
        
        # 实时加载prompt_template
        prompt_template = read_prompt()
        prompt = prompt_template.format(sentence)

        results = generator.text_completion(
            [prompt],
            max_gen_len=MAX_GEN_LEN,
            temperature=TEMPERATURE,
            top_p=TOP_P
        )
        
        for result in results:
            print("llama: {}".format(result['generation']))
            print("\n==================================\n")

if __name__ == '__main__':
    main()