from enum import Enum
from typing import List
from utils.config import LlamaType

import requests

API_URL = "localhost:5000/"

class ApiType(Enum):
    Chat = 'chat'
    Boot = 'boot'
    Check = 'check'

    @property
    def url(self) -> str:
        return API_URL + self.value

def convert(resp: object) -> (int, any):
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
        return self.__call(prompt)

    def __call(self, prompt):
        msg = { "query": prompt }
        resp = requests.post(ApiType.Chat.url, json=msg)

        code, info = resp['code'], resp['info']

        match code:
            case 0: return info
            case 1: raise ValueError(info)
            case _: raise ValueError('Response code {} not known'.format(code))
        
        

        
        