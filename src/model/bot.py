import sys; sys.path.append('.')

import openai
import requests
import json
import random
from abc import abstractmethod
from typing import List
from utils.config import RetrievalType, BotType, Config

def add_division(text: str) -> str:
    DIVISION_TEMPLATE = "{{ {} }}"
    return DIVISION_TEMPLATE.format(text) 

def generate_msg(role: str, content: str):
    return {
        "role": role,
        "content": content
    }

class TSTBot:
    def __init__(self, 
        bot_kind: BotType=None, 
        retrieval_kind: RetrievalType=RetrievalType.Null,
        prompt: str=None, 
        **kwargs
    ):
        self._prompt = prompt
        self._retrieval_kind = retrieval_kind
        self._bot_kind = bot_kind 

        match bot_kind:
            case BotType.GPT:
                self.client = openai.OpenAI(api_key=Config.openai_key)
                self._call = self.__call_gpt
            case BotType.Llama_7B_Chat:
                self.api_url = kwargs['api_url']
                self._call = self.__call_llama2
        
        if retrieval_kind != RetrievalType.Null: self.transfer = self._transfer_retrieval
        match retrieval_kind:
            case RetrievalType.Random:
                random.seed(2017)
                self._retrieval_dataset: List[str] = kwargs['retrieval_dataset']
                self._retrieval = self._retrieval_by_random
            case RetrievalType.BM25:
                from bm25 import BM25
                self._bm25 = BM25(kwargs['retrieval_dataset'])
                self._retrieval = self._retrieval_by_bm25
            case RetrievalType.GTR:
                from chroma import VectorDB
                self._db = VectorDB()
                self.dataset_name = kwargs['dataset_name']
                self._retrieval = self._retrieval_by_gtr
        
    def set_prompt(self, new_prompt: str):
        self._prompt = new_prompt

    def transfer(self, sentence: str, target_style: str, **kwargs):
        if self._prompt is None:
            raise ValueError('The prompt is empty!')
       
        prompt = self._prompt.format(sentence=add_division(sentence), target=target_style)
        return (self._call(prompt), prompt)
    
    def _transfer_retrieval(self, sentence: str, target_style: str, **kwargs):
        if self._prompt is None:
            raise ValueError('The prompt is empty!')
        retrieval_num = 1 if kwargs.get('retrieval_num') == None else kwargs['retrieval_num']
        similar = self._retrieval(sentence, retrieval_num)

        if isinstance(similar, str):
            similar = add_division(similar)
        else: 
            similar = '\n'.join([add_division(s) for s in similar])    
        
        prompt = self._prompt.format(similar=similar, sentence=add_division(sentence), target=target_style)
        return (self._call(prompt), prompt)

    @abstractmethod
    def _call(self, prompt: str):
        pass

    @abstractmethod
    def _retrieval(self, sentence: str, retrieval_num: int) -> str | List[str]:
        pass
                
    def __call_gpt(self, prompt: str) -> str:
        # generate the messages
        messages = []
        # if system_prompt != None:
        #     messages.append(generate_msg("system", system_prompt))
        messages.append(generate_msg("user", prompt))

        response = self.client.chat.completions.create(
            model='gpt-3.5-turbo-0613',
            timeout=5,
            temperature=0,
            stream=False,
            messages=messages
        )

        return response.choices[0].message.content
    
    def __call_llama2(self, prompt: str) -> str:
        def convert(resp: requests.Response) -> (int, any):
            resp = json.loads(resp.text)
            return (resp['code'], resp['info'])

        msg = { "query": prompt }
        resp = requests.post(self.api_url, json=msg)

        code, info = convert(resp)

        match code:
            case 0: return info
            case 1: raise ValueError(info)
            case _: raise ValueError('Response code {} not known'.format(code))

    def _retrieval_by_random(self, sentence: str, retrieval_num: int):
        return random.sample(self._retrieval_dataset, retrieval_num)

    def _retrieval_by_bm25(self, sentence: str, retrieval_num: int):
        return self._bm25.query_top_n(sentence, retrieval_num)
    
    def _retrieval_by_gtr(self, sentence: str, retrieval_num: int):
        return self._db.query(self.dataset_name, sentence, retrieval_num)

if __name__ == '__main__':
    api_url = 'http://localhost:5000/chat'

    bot = TSTBot(BotType.Llama_7B_Chat, RetrievalType.GTR, '{sentence}, {target}, {similar}', api_url=api_url, dataset_name='yelp')
    print(bot.transfer("hello", 'positive'))