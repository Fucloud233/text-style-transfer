import json
import random

from pathlib import Path
from typing import List

random.seed(2017)

def read_lines(file_path: str) -> List[str]: 
    with open(file_path, 'r') as f:
        return f.read(-1).splitlines()

def read_json(file_path: str):
    with open(file_path, 'r') as f:
        return json.load(f)
    
def write_json(file_path: str, json_object):
    with open(file_path, 'w') as f:
        json.dump(json_object, f, indent=4)

def modify_name(origin_file_path: str, file_name: str) -> str:
    file_path = Path(origin_file_path)
    return Path.joinpath(file_path.parent, file_name)

def join_path(path: str, names: List[str] | str):
    path = Path(path)

    if isinstance(names, str):
        return Path.joinpath(path, names)
    
    for name in names:
        path = Path.joinpath(path, name)
    return path

def get_folder(path: str):
    return Path(path).parent

def read_yelp_test_cases(k: int=-1, num: int=2, kind: str='test', is_random=True):
    dataset_path_template = 'data/yelp/sentiment.{}.{}'
    
    test_cases = []
    for i in range(num):
        test_dataset_path = dataset_path_template.format(kind, i)
        test_dataset = read_lines(test_dataset_path)

        sample_sentences = test_dataset
        if is_random:
            sample_sentences = random.sample(test_dataset, int(k/num))
        test_cases.extend([
            {
                "text": sentence,
                "label": i
            } for sentence in sample_sentences
        ])
    
    random.shuffle(test_cases)

    if k != -1:
        test_cases = test_cases[:k]

    return test_cases


def __test_join_path():
    filename = Path('folder/a/b/c')

    assert(filename == join_path('folder', ['a', 'b', 'c']))
    assert(get_folder(filename) == Path('folder/a/b')) 

if __name__ == '__main__':
    __test_join_path()