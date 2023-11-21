import sys
sys.path.append('.')

import random
from utils.file import read_lines, write_lines

def mixer(dataset_folder: str, kind: str):
    random.seed(2017)

    for (i, style_kind) in enumerate(['src', 'tgt']):
        result = []
        for domain in ['em', 'fr']:
            dataset_path = '{}/gyafc_{}/{}.{}'.format(dataset_folder, domain, kind, style_kind)

            lines = read_lines(dataset_path)

            if style_kind == 'tgt' and kind in ['test', 'valid']:
                lines = [eval(line)[0] for line in lines]

            result.extend(lines)

        random.shuffle(result)
        output_path = '{}/gyafc/formality.{}.{}'.format(dataset_folder, kind, i)

        write_lines(output_path, result)

def main():
    dataset_folder = 'data'
    kind = 'test'
    mixer(dataset_folder, kind)

if __name__ == '__main__':
    main()