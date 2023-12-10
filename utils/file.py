import json
import random

from pathlib import Path
from typing import List

random.seed(2017)

def read_lines(file_path: str) -> List[str]: 
    with open(file_path, 'r') as f:
        return f.read(-1).splitlines()
    
def write_lines(file_path: str, lines: List[str]):
    # also create the parent folders
    Path(file_path).parent.mkdir(exist_ok=True, parents=True)

    with open(file_path, 'w') as f:
        for line in lines:
            f.write(line + '\n')

def read_json(file_path: str) -> dict:
    with open(file_path, 'r') as f:
        return json.load(f)
    
def write_json(file_path: str, json_object):
    # also create the parent folders
    Path(file_path).parent.mkdir(exist_ok=True, parents=True)

    with open(file_path, 'w') as f:
        json.dump(json_object, f, indent=4)

def modify_name(origin_file_path: str, file_name: str) -> str:
    file_path = Path(origin_file_path)
    return Path.joinpath(file_path.parent, file_name)

def iter_folder(folder_path: str) -> List[str]:
    return [path.name for path in Path(folder_path).iterdir()]

def fmt_iter_folder(folder_path: str, pattern: str):
    return [(path, path.name) for path in Path(folder_path).glob(pattern)]

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

def load_test_cases(dataset_name: str, k: int=-1, is_random=True):
    dataset_path_template = 'data/{}/test.{}'
    NUM = 2

    test_cases = []
    for i in range(NUM):
        dataset_path = dataset_path_template.format(dataset_name, i)
        dataset = read_lines(dataset_path)

        sample_cases = dataset
        if is_random and k != -1:
            sample_cases = random.sample(sample_cases, int(k/NUM))
        
        test_cases.extend([
            {
                "text": sentence,
                "label": i
            } for sentence in sample_cases
        ])

        # print("len: ", len(test_cases))
    
    random.shuffle(test_cases)

    return test_cases if k == -1 else test_cases[:k]

def __test_join_path():
    filename = Path('folder/a/b/c')

    assert(filename == join_path('folder', ['a', 'b', 'c']))
    assert(get_folder(filename) == Path('folder/a/b')) 

def __test_write_lines():
    file_path = 'output/test.txt'
    lines = ['a', 'b', 'c']
    write_lines(file_path, lines)
    print('hello')

if __name__ == '__main__':
    # __test_join_path()

    print(get_list('output/7b_gyafc_0_1500/bm25'))