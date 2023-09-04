# -*- coding = utf-8 -*-
# @Time : 2023/08/30 22:29
# @Autor : Fucloud
# @FIle : translate.py.py
# @Software : PyCharm

import json
import re
import openai
from tqdm import tqdm
from config import config

openai.api_key = config()["api_key"]
prompt = """
In English, informal and formal text is quite different. Please translate these two types of text below into Chinese while preserving their respective styles.
"""
translate_result = []
informal_file_path = "output/bak/informal.txt"
formal_file_path = "output/bak/formal.txt"


class Translator:
    def __init__(self, json_file_path: str):
        self.informal_file = open(informal_file_path, "a", encoding="utf-8")
        self.formal_file = open(formal_file_path, "a", encoding="utf-8")
        with open(json_file_path, "r") as f:
            self.data = json.load(f)

        self.total_num = 0
        self.success_num = 0

    def run(self, offset: int = 0, length: int = -1):
        def run_translate(text_pair: dict):
            flag = self.__translate(text_pair)
            if flag:
                self.success_num += 1
            self.total_num += 1

        length = length
        if length == -1:
            length = len(self.data)

        for i in tqdm(range(offset, length), desc="[info] 翻译进度: "):
            try:
                run_translate(self.data[i])
            except TimeoutError:
                print("[error] 连接超时...")
            except Exception as e:
                print("[error] ", e)

        # 输出运行结果
        print(f"[info] Result: {self.success_num}/{self.total_num}")

    def __translate(self, text_pair: dict) -> bool:
        def get_text():
            return f"informal: {text_pair['informal']}\nformal: {text_pair['formal']}"

        conversation_list = [{"role": "system", "content": prompt}, {"role": "user", "content": get_text()}]
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=conversation_list)
        answer: str = response.choices[0].message['content']

        # 输出中间结果
        # print_text = answer.replace("\n", " ")
        # print(f'"{print_text}"')

        # 解析输出结果
        try:
            cn_text = extract_input_result(answer)
        except IndexError:
            print("[error] 出现异常: \n{}".format(answer))
            return False

        self.informal_file.write(cn_text["informal"] + '\n')
        self.formal_file.write(cn_text["formal"] + '\n')
        return True
        # translate_result.append(cn_text)


informal_re_pattern = "^(?:informal|Informal|非正式)(?::|：) ?(.*)"
formal_re_pattern = "^(?:formal|Formal|正式)(?::|：) ?(.*)"


# 使用正则表达式提取
def extract_input_result(answer: str) -> dict:
    tmp_lines = answer.splitlines(keepends=False)
    lines = []
    for line in tmp_lines:
        line = line.strip()
        if line != "":
            lines.append(line)

    result = {
        "informal": re.findall(informal_re_pattern, lines[0])[0],
        "formal": re.findall(formal_re_pattern, lines[1])[0]
    }

    return result


# 正则表达式的测试代码
def re_test():
    test_answers = [
        "Informal: 没有其他人和我们一样。\nFormal: 我们是独一无二的，与他人不同。",
        "非正式：我的朋友们说了这个，我简直不敢相信。如果属实，请留下消息来源。谢谢！\n正式：我的朋友们说了这个，我对此表示怀疑。如果是真的，请留下参考来源。谢谢。",
        "informal: 我上了WB的网站，发现《夏之国》不见了。\nformal:《夏之国》已不再在WB的网站上显示。"
    ]
    for test_answer in test_answers:
        try:
            _ = extract_input_result(test_answer)
        except IndexError:
            print("异常:\n" + test_answer)
            return

        print("[info] 成功!")


def main():
    file_path = "output/valid_0_-1.json"
    offset = 536
    # re_test()
    Translator(file_path).run(offset=536)


if __name__ == "__main__":
    main()
