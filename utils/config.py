import sys
sys.path.append(".")

from enum import Enum

from utils.file import read_json, write_json

class BaseConfig(object):
    def __init__(self, file_path):
        obj = read_json(file_path)
        for key in vars(self):
            if key in obj:
                setattr(self, key, obj[key])
    

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

class TransferConfig(BaseConfig):
    def __init__(self, file_path: str):
        self.k = -1

        # record the two different type of style
        self.dataset_path = []
        self.output_path = ""

        self.load_type = None
        self.retrieval_type = None

        self.prompt = ""

        '''
        we will use test datasets to test
        and use train datasets to retrieval,
        so we can't reserve them using 'select index'
        because they're different type of datasets
        '''
        # self.select_index = select_index

        super().__init__(file_path)

        if not self.__check():
            raise ValueError('The number of datasets we can receive is 2!')

        # update the type 
        self.load_type = LoadType(self.load_type)
        self.retrieval_type = RetrievalType(self.retrieval_type)

    def __check(self):
        return len(self.dataset_path) == 2

if __name__ == '__main__':
    Config.load_config_info('config.json')
    print(Config.openai_key)