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
    main()
