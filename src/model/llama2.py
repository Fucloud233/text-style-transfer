from enum import Enum
from pathlib import Path

from llama import Llama
from typing import List

MAX_BATCH_SIZE = 4
MAX_SEQ_LEN = 256
MAX_BATCH_SIZE = 4
MAX_GEN_LEN = None
TEMPERATURE = 0.5
TOP_P = 0.9

class LlamaType(Enum):
    Llama_7B = "llama-2-7b",
    Llama_7B_Chat = "llama-2-7b-chat",

    def ckpt_dir(self):
        return str(Path.joinpath(Path('model'), self.value[0]))

class Llama2:
    def __init__(self, prompt: str, model_type: LlamaType=LlamaType.Llama_7B):        
        self.generator = Llama.build(
            ckpt_dir=LlamaType.ckpt_dir(model_type),
            tokenizer_path="model/tokenizer.model",
            max_seq_len=MAX_SEQ_LEN,
            max_batch_size=MAX_BATCH_SIZE
        )

        self.prompt = prompt

    def transfer(self, sentence):
        prompt = self.prompt.format(sentence)
        return self.__call(prompt)
    
    def __call(self, prompt):
        return self.generator.text_completion(
            [prompt],
            max_gen_len=MAX_GEN_LEN,
            temperature=TEMPERATURE,
            top_p=TOP_P
        )[0]["generation"]