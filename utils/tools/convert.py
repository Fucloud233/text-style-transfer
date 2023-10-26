import json

def convert_eval_prompt_to_json():
    origin_prompts_path = 'data/eval_prompts.origin.txt'
    output_prompts_path = 'data/eval_prompts.json'

    with open(origin_prompts_path, 'r', encoding='utf-8') as f:
        lines = f.read().splitlines()

    count = 0
    cur_type = 0
    prompts_type = [
        'style_transfer_accuracy',
        'content_preservation',
        'fluency'
    ]
    result = {
        'style_transfer_accuracy': [],
        'content_preservation': [],
        'fluency': []
    }
    for line in lines:
        if len(line) == 0 or line.startswith('#'):
            continue
        
        count += 1
        if count % 11 == 0:
            cur_type +=1 

        result[prompts_type[cur_type]].append(line)

    with open(output_prompts_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=4)


if __name__ == '__main__':
    convert_eval_prompt_to_json()