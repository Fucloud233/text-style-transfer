import sys
sys.path.append('.')

from utils.config import Config
import openai

openai.api_key = Config.openai_key

class Bot:
    
    @classmethod
    def talk(self, prompt: str) -> str:
        openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            timeout=5,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Who won the world series in 2020?"},
                {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
                {"role": "user", "content": "Where was it played?"}
            ]
        )

def main():
    Bot.talk("")

if __name__ == '__main__':
    # print('hello')
    # print(openai.api_key)
    # print(openai.Model.list())
    main()


