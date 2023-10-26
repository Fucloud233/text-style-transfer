import sys
sys.path.append('.')

from utils.config import Config
import openai

openai.api_key = Config.openai_key


class Bot:
    model_type = "gpt-3.5-turbo-0613"
    
    @classmethod
    def ask(self, system_prompt: str, prompt: str) -> str:
        response = openai.ChatCompletion.create(
            model=Bot.model_type,
            timeout=5,
            temperature=0,
            messages=[
                {
                    "role": "system", 
                    "content": system_prompt
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ]
        )

        return response['choices'][0]['message']['content']
    