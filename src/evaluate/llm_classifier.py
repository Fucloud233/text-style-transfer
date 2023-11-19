import sys; sys.path.append("."); sys.path.append("./src")


import random

from tqdm import tqdm

from utils.file import read_json, read_lines
from bot import Bot

'''
here is a sentence: {it just gets worse .}.
it's negative or positive:{
'''

random.seed(2017)

def evaluate(
    sentences_path: str,
    prompt_template: str,
    system_prompt: str=None
):  
    sentences = read_json(sentences_path)

    for sentence in tqdm(sentence, desc="process"):
        prompt = prompt_template.format(sentence=sentence)
        answer = Bot.ask(prompt, system_prompt)

        print(answer)


def test(
    sentence: str,
    prompt_template: str,
    system_prompt: str=None
):
    prompt = prompt_template.format(sentence=sentence)
    return Bot.ask(prompt, system_prompt)

def test_runner():
    prompt_template = "here is a sentence: {sentence}. it's negative or positive:{{"
    system_prompt = "Here are some questions below, you should directly answer negative or positive."

    while True:
        sentence = input("input: ")
        result = test(sentence, prompt_template, system_prompt)
        print("bot:", result)


def test_bot():
    k = 100
    num = 2
    test_dataset_path_template = 'data/yelp/sentiment.test.{}'
    
    test_cases = []
    for i in range(num):
        test_dataset_path = test_dataset_path_template.format(i)
        test_dataset = read_lines(test_dataset_path)

        sample_sentences = random.sample(test_dataset, int(k/num))
        test_cases.extend([
            {
                "text": sentence,
                "label": i
            } for sentence in sample_sentences
        ])
    
    random.shuffle(test_cases)

    counter = 0
    total = k
    for test_case in tqdm(test_cases, desc="process"):
        prompt_template = "here is a sentence: {sentence}. it's negative or positive:{{"
        system_prompt = "Here are some questions below, you should directly answer negative or positive."

        try:
            answer = Bot.ask(prompt_template.format(sentence=test_case['text']), system_prompt)

            if not ((answer.strip() == 'negative') ^ (test_case['label'] == 0)):
                counter += 1
        except Exception as e:
            print(e)
            total -= 1
            continue

    print("accuracy: {} ({}/{})".format(counter/total, counter, total))

    
if __name__ == '__main__':
    # print(random.randint(0, 10))
    test_bot()