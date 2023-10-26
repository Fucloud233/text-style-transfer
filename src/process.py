import json

END_SYMBOL = '}'

def load_sentences(file_path: str) -> list[dict[str, str]] :
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)
    
def save_sentence(file_path: str, sentences):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(sentences, f, indent=4)
    
def process():
    raw_file_path = 'output/7b_chat_yelp/test.0.raw.json'
    output_file_path = 'output/7b_chat_yelp/test.0.json'

    raw_sentences = load_sentences(raw_file_path)

    sentences = []
    for r_s in raw_sentences:
        sentences.append({
            '0': r_s['0'].split(END_SYMBOL)[0],
            '1': r_s['1'].split(END_SYMBOL)[0]
        })

    save_sentence(output_file_path, sentences)
    
    print('Save Over!')

if __name__ == '__main__':
    process()
    
    