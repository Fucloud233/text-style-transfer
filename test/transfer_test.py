import sys
sys.path.append('.')
sys.path.append('src')

from utils.config import TransferConfig
from transfer import select_bot, transfer

def main(config_path: str):
    config = TransferConfig(config_path)
                     
    bot = select_bot(config.prompt, config.llama_type, 
        config.retrieval_type, config.retrieval_path)

    while True:
        sentence = input("input: ")
        if sentence == "exit":
            break
        
        (result, prompt) = transfer(bot, sentence)

        print("prompt:", prompt)
        print("result: ", result)

if __name__ == '__main__':
    config_path = 'output/7b_chat_yelp/test.0/100/bm25/transfer_config.json'
    main(config_path)