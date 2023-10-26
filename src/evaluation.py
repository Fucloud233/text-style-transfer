import sys
sys.path.append('.')

from utils.file import read_json, write_json

EVAL_TYPE = [
    'style_transfer_accuracy',
    'content_preservation',
    'fluency'
]


def generate_prompt(input: str, transferred: str, prompt_template=str):
    prompt = prompt_template
    prompt = prompt.replace(f"{{input}}", input)
    prompt = prompt.replace(f"{{transferred}}", transferred)

    return prompt

def main():
    prompt_tempalates_path = 'data/eval_prompts.json'
    sentences_path = 'output/7b_chat_yelp/test.0.json'

    all_prompt_tempalates = read_json(prompt_tempalates_path)
    sentences = read_json(sentences_path)

    counter = 0
    
    # 先选择Evaluation Type
    for eval_type in EVAL_TYPE:
        prompt_templates = all_prompt_tempalates[eval_type]

        for sentence in sentences:
            for prompt_template in prompt_templates:
                counter += 1

                if counter >= 10:
                    break
                
                prompt = generate_prompt(sentence['0'], sentence['1'], prompt_template)
                
                print(prompt)


if __name__ == '__main__':
    main()
            
            