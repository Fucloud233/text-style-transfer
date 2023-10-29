import sys
sys.path.append('.')

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

def test_eval_d():
    for d in EvalD:
        print(d.value)
    
def main():
    # test_eval_d()
    data_path = "output/7b_chat_yelp/test.0.eval_result.raw.json"
    output_path = "output/7b_chat_yelp/test.0.eval_result.json"

    result = calculate(data_path)

    write_json(output_path, result)
    
    pass

if __name__ == '__main__':
    main()