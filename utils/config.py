import sys
sys.path.append(".")

from enum import Enum
from pathlib import Path
from utils.file import read_json, write_json

class BaseConfig(object):
    def __init__(self, json_obj):
        # if receive a path, it will convert it to object
        if isinstance(json_obj, str):
            obj = read_json(json_obj)

        for key in vars(self):
            if key not in obj:
                continue
            attr = getattr(self, key)
            if isinstance(attr, Enum):
                setattr(self, key, type(attr)(obj[key]))
            else:
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

class LlamaType(Enum):
    Llama_7B = "llama-2-7b"
    Llama_7B_Chat = "llama-2-7b-chat"

    def ckpt_dir(self):
        return str(Path.joinpath(Path('model'), self.value))


class TransferConfig(BaseConfig):
    def __init__(self, file_path: str):
        self.k = -1

        # record the two different type of style
        self.dataset_path = ""
        self.retrieval_path = ""
        self.output_path = ""

        self.load_type = LoadType.Front
        self.retrieval_type = RetrievalType.Null
        self.llama_type = LlamaType.Llama_7B_Chat

        self.prompt = ""

        super().__init__(file_path)

class BootConfig(BaseConfig):
    def __init__(self, json_obj):
        self.llama_type = LlamaType.Llama_7B_Chat
        super().__init__(json_obj)

if __name__ == '__main__':
    Config.load_config_info('config.json')
    print(Config.openai_key)