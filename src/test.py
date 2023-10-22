from llama import Llama
from typing import List

MAX_BATCH_SIZE = 4

MAX_GEN_LEN: int = 64
TEMPERATURE = 0.5
TOP_P = 0.9

def main():
    generator = Llama.build(
        ckpt_dir="llama-2-7b-chat/",
        tokenizer_path="tokenizer.model",
        max_seq_len=256,
        max_batch_size=4
    )


    while True:
        prompts: List[str] = []
        
        question = ""
        print("Your: ", end="")
        while True:
            line = input()
            if line.strip() == '$':
                break

            question += line
        
        if question == 'exit':
            break
        
        prompts.append(question)

        results = generator.text_completion(
            prompts,
            max_gen_len=MAX_GEN_LEN,
            temperature=TEMPERATURE,
            top_p=TOP_P
        )
        
        for result in results:
            print("llama: {}".format(result['generation']))
            print("\n==================================\n")

if __name__ == '__main__':
    main()