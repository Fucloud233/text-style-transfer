from utils.config import LlamaType
from llama import Llama

MAX_BATCH_SIZE = 4
MAX_SEQ_LEN = 512
MAX_BATCH_SIZE = 4
MAX_GEN_LEN = None
TEMPERATURE = 0.5
TOP_P = 0.9

class Llama2:
    def __init__(self, model_type: LlamaType=LlamaType.Llama_7B):  
        self.model_type = model_type
        self.generator = None

    def boot(self, llama_type: LlamaType):
        
        self.model_type = llama_type

        self.generator = Llama.build(
            ckpt_dir=LlamaType.ckpt_dir(self.model_type),
            tokenizer_path="model/tokenizer.model",
            max_seq_len=MAX_SEQ_LEN,
            max_batch_size=MAX_BATCH_SIZE
        )

    def chat(self, prompt):
        return self.generator.text_completion(
            [prompt],
            max_gen_len=MAX_GEN_LEN,
            temperature=TEMPERATURE,
            top_p=TOP_P
        )[0]["generation"]
    
    @property
    def is_running(self):
        return self.generator != None
    
    