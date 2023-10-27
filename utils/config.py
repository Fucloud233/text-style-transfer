import sys
sys.path.append(".")

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

if __name__ == '__main__':
    Config.load_config_info('config.json')
    print(Config.openai_key)