import sys
sys.path.append('.')

import pandas as pd
import numpy as np

from utils.file import read_json, write_json
from utils.evaluate import EvalD


def calculate(data_path: str):
    data_list = read_json(data_path)

    total_scores = {
        "style": .0,
        "content": .0,
        "fluency": .0,
    }

    for data in data_list:
        for d in EvalD:
            sum = 0
            counter = 0
            for score in data['score'][d.value]:
                try:
                    score = float(score)
                except ValueError:
                    # 如果说出现解析失败的情况则跳过
                    continue

                # 归一化
                if score >= 1:
                    score = score / 5

                counter += 1
                sum += score
            
            total_scores[d.value] += sum / counter

    total = len(data_list)
    result = {
        "total": total
    }
    for d in EvalD:
        result[d.value] = total_scores[d.value] / total

    return result

def calculate_in_csv(data_path: str):
    data_list = pd.read_csv(data_path)
    data_list = data_list.to_numpy().reshape((-1, 3))[:, 1:]

    # 对数据进行归一化

    result = {
        "total": len(data_list) / 33
    }

    for eval_d in EvalD:
        # 选择对应标签的内容
        data = data_list[data_list[:, 0] == eval_d.value][:, 1]
        # 去除无效值
        data = data[data > 0]
        # 归一化
        data[data>=1] = data[data>=1] / 5    
        # 计算平均值
        result[eval_d.value] = np.average(data)
                     
    return result


def test_eval_d():
    for d in EvalD:
        print(d.value)
    
def main():
    # test_eval_d()
    data_path = "output/7b_chat_yelp/test.0/100/result.raw.csv"
    output_path = "output/7b_chat_yelp/test.0/100/result.json"

    result = calculate_in_csv(data_path)

    write_json(output_path, result)
    
    pass

if __name__ == '__main__':
    main()