import sys
sys.path.append('.')

from flask import Flask
from flask import request
from utils.config import BootConfig
from server.bot import Llama2

llama = Llama2()

app = Flask("llama")

def gen_return_data(info: str, code: int):
    return {
        "code": code,
        "info": info
    }

@app.route("/hello")
def hello_word():
    return "Hello, World!"

@app.route("/boot", methods=['POST'])
def boot():
    config = BootConfig(request.get_json())
    
    if llama.is_running:
        return gen_return_data("Llama2 is running!", 1)
    
    llama.boot(config.llama_type)
    return gen_return_data('{} boot successful!'.format(config.llama_type.name), 0)
    
@app.route("/check", methods=['GET'])
def check():
    return gen_return_data(llama.is_running, 0)

@app.route("/chat", methods=['POST'])
def chat():
    try:
        query = request.get_json()['query']
        if len(query) == 0:
            raise ValueError('The query is empty!')    
        answer = llama.chat(query)
        return gen_return_data(answer, 0)
    except Exception as e:
        return gen_return_data(repr(e), 0)

if __name__ == '__main__':
    app.run(port=5000, host="0.0.0.0", debug=False)