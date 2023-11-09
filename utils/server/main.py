import sys
sys.path.append('.')

from flask import Flask
from flask import request
from utils.config import BootConfig
from utils.server.bot import Llama2

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
    
    llama.boot()
    return gen_return_data('Llama2 boot successful!', 0)

@app.route("/chat", methods=['POST'])
def chat():
    try:
        query = request.get_json()['query']
    except:
        return gen_return_data('The query is empty!', 1)

    answer = llama.chat(query)
    return gen_return_data(answer, 0)

if __name__ == '__main__':
    app.run(port=5000, host="0.0.0.0", debug=False)