from utils.file import read_json

class Config:
    __config_info = read_json('config.json')

    @classmethod
    @property
    def openai_key(self):
        return Config.__config_info['openai-key']

''' config.json
For example: 

{
    "openai-key": "sk-xxx"
}
'''