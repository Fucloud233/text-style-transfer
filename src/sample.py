# TODO: choose n pieces of data from dataset for fixed result

import sys
sys.path.append('.')

import random
from utils.file import read_lines, write_lines
from utils.config import LoadType

def sample_dataset(dataset_path: str, k: int=-1, is_random: bool=True):
    lines = read_lines(dataset_path)
    
    if k == -1:
        return lines
    elif is_random:
        return random.sample(lines, k)
    else:
        return lines[:k]

def run(
    dataset_name: str,
    dataset_kind: str='test', 
    style_kind: int=0,
    output_name: str=None, 
    k: int=-1, 
    is_random: bool=True
):  
    # generate filename automatically
    dataset_path = 'data/{}/{}.{}'.format(dataset_name, dataset_kind, style_kind)
    output_path = 'output/{}'.format(output_name) if output_name != None \
        else 'output/{}.{}.{}.{}'.format(dataset_name, dataset_kind, style_kind, k)

    dataset = sample_dataset(dataset_path, k, is_random)
    write_lines(output_path, dataset)

def main():
    random.seed(2017)

    dataset_name = 'gyafc'
    k = 1500

    run(dataset_name, k=k)

if __name__ == '__main__':


    main()
