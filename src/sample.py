# TODO: choose n pieces of data from dataset for fixed result

import sys
sys.path.append('.')

import random
from utils.config import LoadType

def sample_dataset(dataset_path: str, k: int=-1, load_type: LoadType=LoadType.Front):
    with open(dataset_path, 'r', encoding='utf-8') as f:
        # 选择前k条
        if (load_type == LoadType.Front):
            if k == -1:
                return f.read(-1).splitlines()

            return [f.readline().strip() for _ in range(k)]
        # 随机选择
        elif (load_type == LoadType.Random):
            dataset = f.read().splitlines()
            return random.sample(dataset, k)
        else:
            return None
        

def save_dataset(save_path: str, dataset: list[str]):
    with open(save_path, 'w', encoding='utf-8') as f:
        for line in dataset:
            f.write(line + '\n')

def run(load_path: str, output_path: str, k: int, load_type: LoadType):
    if load_path == '' or output_path == '':
        print('The parameter is empty!')
        return

    dataset = sample_dataset(load_path, k, load_type)
    save_dataset(output_path, dataset)


def main():
    load_path = ''
    output_path = ''
    
    k = 100
    load_type = LoadType.Random

    run(load_path, output_path, k, load_type)

if __name__ == '__main__':


    main()
