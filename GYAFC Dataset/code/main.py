# -*- coding = utf-8 -*-
# @Time : 2023/07/26 16:23
# @Autor : Fucloud
# @FIle : main.py.py
# @Software : PyCharm

from pathlib import Path
import json

src_suffix = '.src'
tgt_suffix = '.tgt'


class DatasetHandler:
    def __init__(self, _base_file_path: str, _dataset_type: str, prompt: str = "", _output_path: str = 'output',
                 offset: int = 0, size: int = 10):
        self.base_file_path = Path(_base_file_path)
        self.output_path = Path(_output_path)
        self.dataset_type = _dataset_type

        self.prompt = prompt

        # 记录读取数据在 大小和偏移量
        self.offset = offset
        self.size = size

        self.src_label = "informal"
        self.tgt_label = "formal"

    # 主函数
    def handle(self):
        src_list, tgt_list = self.load_data()
        # json_data = self.data_to_json(src_list, tgt_list)
        # self.save_json(json_data)
        self.save_plain(src_list, tgt_list)

    # 从文件中读取两种风格的数据
    def load_data(self) -> tuple[list[str], list[str]]:
        file_path = Path(Path.joinpath(self.base_file_path, self.dataset_type))

        src_path = file_path.with_suffix(src_suffix)
        tgt_path = file_path.with_suffix(tgt_suffix)

        if not (src_path.exists() and tgt_path.exists()):
            return [], []

        # print("[debug] file exists!")

        src_list = self.read_lines(src_path)
        tgt_list = self.read_lines(tgt_path)

        # for i in range(max_length):
        #     print("[debug]\n src: {} \n tgt: {}".format(src_list[i], tgt_list[i]))

        return src_list, tgt_list

    # 读取文件中每一行
    def read_lines(self, file_path: Path) -> list[str]:
        result_list = []

        with file_path.open("r") as src_f:
            # 先读取到对应的偏移量
            for i in range(0, self.offset):
                src_f.readline()

            for i in range(0, self.size):
                line = src_f.readline().strip()

                if line == "":
                    break

                result_list.append(line)

        return result_list

    # 将读取到的数据转换为json格式
    def data_to_json(self, src_list: list[str], tgt_list: list[str]) -> str:
        size = len(src_list)
        json_list = []
        for i in range(size):
            json_list.append({
                self.src_label: src_list[i],
                self.tgt_label: tgt_list[i]
            })

        return json.dumps(json_list, indent=4, separators=(',', ':'))

    # 保存json文件
    def save_json(self, json_data: str) -> None:
        if not self.output_path.exists():
            self.output_path.mkdir()

        # print("[debug] json: ", json_data)
        file_name = "{}_{}_{}.json".format(self.dataset_type, self.offset, self.offset+self.size)
        file_path = Path.joinpath(Path('output'), file_name)
        with open(file_path, "w") as f:
            f.write(json_data)

    #  保存为普通的数据
    def save_plain(self, src_list: list[str], tgt_list: list[str]) -> None:
        if not self.output_path.exists():
            self.output_path.mkdir()

        file_name = "{}_{}_{}.txt".format(self.dataset_type, self.offset, self.offset+self.size)
        file_path = Path.joinpath(Path('output'), file_name)
        with open(file_path, "w") as f:
            # 先输出prompt
            if prompt != "":
                f.write(prompt + "\n\n")

            for i in range(len(src_list)):
                f.write("{}: {}\n{}: {}\n\n".format(
                    self.src_label, src_list[i],
                    self.tgt_label, tgt_list[i]
                ))

        print(f"[info] Output {file_path} Success!")


if __name__ == "__main__":
    # 数据集所在的路径
    base_file_path = "dataset/gyafc_em"
    # 数据集对应的类型
    dataset_type = "train"

    # 输入的提示词 (用于输入给ChatGPT)
    # 如果不需要 留空即可
    prompt = "In English, informal and formal text is quite different. " \
             "Please translate these two types of text below into Chinese while preserving their respective styles.\n" \
             "Remember use the format we give to output."

    # 读取数据集的位置(偏移量)和大小
    offset = 0
    size = 10

    # 运行程序
    handler = DatasetHandler(base_file_path, dataset_type,
                             prompt=prompt, offset=offset, size=size)
    handler.handle()
