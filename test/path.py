from enum import Enum
from pathlib import Path

class LlamaType(Enum):
    Llama_7B = "llama-2-7b",
    Llama_7B_Chat = "llama-2-7b-chat",

    def ckpt_dir(self):
        return str(Path.joinpath(Path('model'), self.value[0]))

def test_path():
    print(LlamaType.ckpt_dir(LlamaType.Llama_7B))

if __name__ == '__main__':
    test_path()
    