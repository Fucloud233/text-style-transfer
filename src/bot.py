import sys
sys.path.append('.')

from utils.config import Config
import openai

# Migration Guide: https://github.com/openai/openai-python/discussions/742

def generate_msg(role: str, content: str):
    return {
        "role": role,
        "content": content
    }

class Bot:
    model_type = "gpt-3.5-turbo-0613"

    client = openai.OpenAI(
        api_key=Config.openai_key
    )
    
    @classmethod
    def ask(self, prompt: str, system_prompt: str=None) -> str:
        # generate the messages
        messages = []
        if system_prompt != None:
            messages.append(generate_msg("system", system_prompt))
        messages.append(generate_msg("user", prompt))

        response = Bot.client.chat.completions.create(
            model=Bot.model_type,
            timeout=5,
            temperature=0,
            stream=False,
            messages=messages
        )

        return response.choices[0].message.content
    