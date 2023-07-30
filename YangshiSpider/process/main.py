# -*- coding = utf-8 -*-
# @Time : 2023/07/30 10:52
# @Autor : Fucloud
# @FIle : main.py
# @Software : PyCharm

import pandas
import os
from pathlib import Path
from word_counter import WordCounter


class YangshiDataHandler:
    def __init__(self, input_file_name: str, output_file_name: str = None,
                 length_range: tuple[int, int] = (-1, -1)):
        self.counter = WordCounter()
        self.input_file_name = Path(input_file_name)

        # 如果没有传入输出路径 则修改文件路径输出
        self.output_suffix = ".tgt"
        if output_file_name is not None:
            self.output_file_name = output_file_name
        else:
            self.output_file_name = self.input_file_name.with_suffix(self.output_suffix)

        self.contents = None
        self.length_range = length_range

    def handle(self):
        # print("[debug] pwd", os.path.abspath("."))
        # 读取数据
        self.read_contents()
        # 预处理数据
        self.pre_process_data()
        print("[info] the number of contents: ", len(self.contents))
        # 保存数据
        self.save_data()

        # for content in contents:
        #     print("[debug] content: ", content)
        # counter.display()
        # 显示数据分布情况
        self.counter.display_graph()

    # 读取文件中的content数据
    def read_contents(self):
        data_frame = pandas.read_csv(self.input_file_name, dtype="string")
        self.contents = data_frame["content"]

    # 数据的预处理
    def pre_process_data(self):
        output_content = []

        for content in self.contents:
            # 根据段进行划分
            # print("[debug] type = {}, result = {}".format(type(content),  isinstance(content, str)))
            if content is None or not isinstance(content, str):
                continue
            lines = content.split("\n")

            for line in lines:
                line = line.strip()
                line_length = len(line)
                # 检验句子长度
                if self.check_length(line_length):
                    continue

                output_content.append(line)
                # 统计长度
                self.counter.add_text(line)

        self.contents = output_content

    # 数据的保存
    def save_data(self):
        with open(self.output_file_name, 'w', encoding="utf-8") as f:
            for line in self.contents:
                f.write(line + "\n")

    # 验证长度是否有效
    def check_length(self, length: int) -> bool:
        if self.length_range[0] == -1 or self.length_range[1] == -1:
            return length == 0

        return length < self.length_range[0] or length > self.length_range[1]


if __name__ == "__main__":
    input_file_name = "output/yangshi_news_tech.csv"
    handler = YangshiDataHandler(input_file_name, length_range=(25, 225))
    handler.handle()
