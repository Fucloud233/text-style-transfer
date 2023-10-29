import sys
sys.path.append(".")

from enum import Enum

from utils.file import read_json, write_json

class Config:
    __config_info: dict = None

    @classmethod
    @property
    def openai_key(cls):
        return cls.__config_info.get('openai-key')

    @staticmethod
    def load_config_info(config_path: str):
        try:
            Config.__config_info = read_json(config_path)
        except FileNotFoundError:
            config_template = {
                "openai-key": "sk-xxx"    
            }
            
            write_json(config_path, config_template)
            raise FileNotFoundError("Config file has been not initialized!")

''' config.json
For example: 

{
    "openai-key": "sk-xxx"
}
'''

class LoadType(Enum):
    Front = 'front'
    Random = 'random'

class TransferConfig:
    def __init__(self, k: int, load_type: LoadType, 
            dataset_path: str, output_path: str):
        self.k = k
        self.dataset_path = dataset_path
        self.output_path = output_path
        self.load_type = load_type
        # load_type: LoadType

    @staticmethod
    def from_file(file_path: str):
        info = read_json(file_path)

        return TransferConfig(
            info['k'],
            LoadType(info['load_type']),
            info['dataset_path'],
            info['output_path']
        )

if __name__ == '__main__':
    Config.load_config_info('config.json')
    print(Config.openai_key)