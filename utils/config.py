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

class RetrievalType(Enum):
    BM25 = 'bm25'
    Null = 'null'


'''
dataset_path: {
    [
        "dataset_path_0",
        "dataset_path_1"
    ]
}

'''

class TransferConfig:
    def __init__(self, k: int, load_type: LoadType, 
            dataset_path: list[str],  output_path: str,
            select_index: int, retrieval_type: RetrievalType
        ):
        self.k = k
        
        # record the two different type of style
        self.dataset_path = dataset_path

        self.output_path = output_path
        self.load_type = load_type

        self.select_index = select_index
        self.retrieval_type = retrieval_type

    @staticmethod
    def from_file(file_path: str):
        info = read_json(file_path)

        config = TransferConfig(
            info['k'],
            LoadType(info['load_type']),
            info['dataset_path'],
            info['output_path'],
            info['select_index'],
            RetrievalType[info['retrieval_type']]
        )

        if not config.__check():
            raise ValueError('The number of datasets we can receive is 2!')

        return config

    def __check(self):
        return len(self.dataset_path) == 2 \
            and self.select_index in [0, 1]
    
    @property
    def another_index(self):
        return self.load_type & 1

if __name__ == '__main__':
    Config.load_config_info('config.json')
    print(Config.openai_key)