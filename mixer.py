from typing import List
import random

LABEL = '__label__'

def read_lines(file_path: str):
    with open(file_path ,'r', encoding='utf-8') as f:
        return f.read(-1).splitlines()

def write_lines(lines: List[str], file_path: str):
    with open(file_path, 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line + '\n')

def run(style_paths: List[str], style_kinds: List[str], output_path: str):
    
    result = []
    for (path, kind) in zip(style_paths, style_kinds):
        lines = read_lines(path)
        lines = [LABEL + kind + ' ' + line for line in lines]
        result.extend(lines)
    
    random.shuffle(result)

    write_lines(result, output_path)

def generate_data(kind: str, sentence: str):
    return LABEL + kind + ' ' + sentence


# src: informal tgt: formal
def gyafc_em_mixer():
    dataset_path = 'data/gyafc_em/{}'
    dataset_kinds = ['src', 'tgt']
    style_kinds = ['informal', 'formal']

    # train dataset
    train_dataset_path = 'data/gyafc_em/train.{}'

    train_result = []
    for (dataset_kind, style_kind) in zip(dataset_kinds, style_kinds):
        lines = read_lines(train_dataset_path.format(dataset_kind))
        lines = [generate_data(style_kind, line) for line in lines]
        train_result.extend(lines)
    
    random.shuffle(train_result)

    write_lines(train_result, dataset_path.format('formality.train'))

    # test_dataset
    test_dataset_path = 'data/gyafc_em/test.{}'

    test_result = []
    for (dataset_kind, style_kind) in zip(dataset_kinds, style_kinds):
        lines = read_lines(test_dataset_path.format(dataset_kind))
        # we choose the first in the tgt output
        lines = [generate_data(style_kind, line) for line in lines] if dataset_kind == 'src' \
            else [generate_data(style_kind, eval(line)[0]) for line in lines] 
        test_result.extend(lines)
    
    random.shuffle(test_result)

    write_lines(test_result, dataset_path.format('formality.test'))

def main():

    style_kinds = ['negative', 'positive']

    dataset_kinds = ['train', 'test']
    
    for kind in dataset_kinds:
        style_paths = [
            'data/yelp/sentiment.{kind}.0'.format(kind=kind),
            'data/yelp/sentiment.{kind}.1'.format(kind=kind),
        ]

        output_path = 'data/yelp/sentiment.{kind}'.format(kind=kind)\

        run(
            style_paths, 
            style_kinds, 
            output_path
        )


if __name__ == '__main__':
    random.seed(2017)
    # main()
    gyafc_em_mixer()
