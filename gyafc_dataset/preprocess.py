# -*- coding = utf-8 -*-
# @Time : 2023/08/30 22:31
# @Autor : Fucloud
# @FIle : mix_dataset.py.py
# @Software : PyCharm

import json
from enum import Enum
from pathlib import Path


class OutputType(Enum):
    Json = 0
    Plain = 1


class DatasetType(Enum):
    test = "test"
    train = "train"
    valid = "valid"


src_suffix = '.src'
tgt_suffix = '.tgt'

src_label = "informal"
tgt_label = "formal"


class DatasetHandler:
    def __init__(self, base_file_path: str, dataset_type: DatasetType, output_name: str,
                 output_type: OutputType = OutputType.Json,
                 output_path: str = 'output',
                 read_offset: int = 0, read_size: int = 10):
        self.base_file_path = Path(base_file_path)
        self.output_name = output_name
        self.output_path = Path(output_path)
        self.dataset_type = dataset_type
        self.output_type = output_type

        # 记录读取数据在 大小和偏移量
        self.offset = read_offset
        self.size = read_size

    # 主函数
    def handle(self):
        src_list, tgt_list = self.load_data()
        if self.output_type == OutputType.Json:
            self.save_json(src_list, tgt_list)
        elif self.output_type == OutputType.Plain:
            self.save_plain(src_list, tgt_list)

    # 从文件中读取两种风格的数据
    def load_data(self) -> tuple[list[str], list[str]]:
        file_path = Path(Path.joinpath(self.base_file_path, self.dataset_type.name))

        src_path = file_path.with_suffix(src_suffix)
        tgt_path = file_path.with_suffix(tgt_suffix)

        if not (src_path.exists() and tgt_path.exists()):
            return [], []

        # print("[debug] file exists!")

        src_list = self.read_lines(src_path)
        tgt_list = self.read_lines(tgt_path)
        if self.dataset_type is DatasetType.valid:
            tgt_list = select_first(tgt_list)

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

            lines = src_f.readlines(self.size)
            for line in lines:
                result_list.append(line.strip())

        return result_list

    #  保存为普通的数据
    def save_plain(self, src_list: list[str], tgt_list: list[str]) -> None:
        if not self.output_path.exists():
            self.output_path.mkdir()

        file_name = "{}_{}".format(self.output_name, self.dataset_type.name)
        if self.size != -1:
            file_name += "_{}_{}".format(self.offset, self.offset+self.size)
        file_name += ".txt"

        file_path = Path.joinpath(Path('output'), file_name)
        with open(file_path, "w") as f:

            for i in range(len(src_list)):
                f.write("{}: {}\n{}: {}\n\n".format(
                    src_label, src_list[i],
                    tgt_label, tgt_list[i]
                ))

        print(f"[info] Output {file_path} Success!")

    # 保存json文件
    def save_json(self, src_list: list[str], tgt_list: list[str]) -> None:
        # 将读取到的数据转换为json格式
        def data_to_json() -> str:
            json_list = []
            for i in range(len(src_list)):
                json_list.append({
                    src_label: src_list[i],
                    tgt_label: tgt_list[i]
                })

            return json.dumps(json_list, indent=4, separators=(',', ':'))

        # 首先转换为json格式
        json_data = data_to_json()

        if not self.output_path.exists():
            self.output_path.mkdir()

        file_name = "{}_{}_{}.json".format(self.dataset_type.name, self.offset, self.offset + self.size)
        file_path = Path.joinpath(Path('output'), file_name)
        with open(file_path, "w") as f:
            f.write(json_data)


def select_first(lines: list[str]) -> list[str]:
    output_list = []
    for line in lines:
        output_list.append(eval(line)[0])
    return output_list


def main():
    # 数据集所在的路径
    base_file_path = "dataset/gyafc_em"
    # 数据集对应的类型
    dataset_type = DatasetType.valid
    # 输出文件名
    output_name = "em"

    # 读取数据集的位置(偏移量)和大小
    size = -1
    # 运行程序
    handler = DatasetHandler(base_file_path, dataset_type, output_name,
                             read_size=size,
                             output_type=OutputType.Json)
    handler.handle()


if __name__ == "__main__":
    main()
