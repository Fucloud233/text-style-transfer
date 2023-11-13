import sys
sys.path.append('.')

from utils.config import Config
import openai

# Migration Guide: https://github.com/openai/openai-python/discussions/742

class Bot:
    model_type = "gpt-3.5-turbo-0613"

    client = openai.OpenAI(
        api_key=Config.openai_key
    )
    
    @classmethod
    def ask(self, prompt: str, system_prompt: str="") -> str:
        response = Bot.client.chat.completions.create(
            model=Bot.model_type,
            timeout=5,
            temperature=0,
            stream=False,
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

        return response.choices[0].message.content
    