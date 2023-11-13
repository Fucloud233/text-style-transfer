import json
import requests

from enum import Enum
from utils.config import LlamaType

# https://requests.readthedocs.io/en/latest/user/quickstart/

# remember use 'http://' prefix
API_URL = "http://localhost:5000/"

class ApiType(Enum):
    Chat = 'chat'
    Boot = 'boot'
    Check = 'check'

    @property
    def url(self) -> str:
        return API_URL + self.value

def convert(resp: requests.Response) -> (int, any):
    resp = json.loads(resp.text)
    return (resp['code'], resp['info'])

def init_status():
    resp = requests.get(ApiType.Check.url)
    (_, is_running) = convert(resp)
    return is_running

class Llama2:
    __status = init_status()

    def __init__(self, prompt: str, model_type: LlamaType=LlamaType.Llama_7B):
        self.prompt = prompt
        
        if Llama2.__status:
           return 
        
        msg = { 'llama_type': model_type.value }
        (code, _) = convert(requests.post(ApiType.Boot.url, msg))
        if code == 0:
            Llama2.__status = True

    def transfer(self, sentence):
        prompt = self.prompt.format(sentence)
        return (self._call(prompt), prompt)
    
    def _call(self, prompt):
        msg = { "query": prompt }
        resp = requests.post(ApiType.Chat.url, json=msg)

        code, info = convert(resp)

        match code:
            case 0: return info
            case 1: raise ValueError(info)
            case _: raise ValueError('Response code {} not known'.format(code))