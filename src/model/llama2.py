import sys; sys.path.append('.')

import json
import requests

from enum import Enum
from utils.config import RetrievalType

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

DIVISION_TEMPLATE = "{{ {} }}"

def add_division(text: str) -> str:
    return DIVISION_TEMPLATE.format(text)

class Llama2:
    def __init__(self, prompt: str=None):
        self._prompt = prompt
        self._type = RetrievalType.Null

    def transfer(self, sentence: str, target_style: str):
        if self._prompt is None:
            raise ValueError('The prompt is empty!')

        # append division for sentence
        prompt = self._prompt.format(sentence=add_division(sentence), target=target_style)
        return (self._call(prompt), prompt)
    
    def _call(self, prompt):
        msg = { "query": prompt }
        resp = requests.post(ApiType.Chat.url, json=msg)

        code, info = convert(resp)

        match code:
            case 0: return info
            case 1: raise ValueError(info)
            case _: raise ValueError('Response code {} not known'.format(code))

    def set_prompt(self, new_prompt: str):
        self._prompt = new_prompt

    @property
    def type(self):
        return self._type

def test_display_type():
    llama2 = Llama2("a")
    print(llama2.type)

if __name__ == '__main__':
    test_display_type()