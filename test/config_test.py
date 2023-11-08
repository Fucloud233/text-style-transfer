import sys
sys.path.append('.')

from pprint import pprint

from utils.config import Config
from utils.config import TransferConfig

def test_transfer_config():
    config_path = 'output/7b_chat_yelp/test.0/100/bm25/transfer_config.json'
    config_info = TransferConfig(config_path)
    
    # using vars() to get the all properties in a class
    pprint(vars(config_info))

if __name__ == '__main__':
    # print(Config.openai_key)
    test_transfer_config()
