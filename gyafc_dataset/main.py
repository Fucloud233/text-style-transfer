# -*- coding = utf-8 -*-
# @Time : 2023/08/30 23:50
# @Autor : Fucloud
# @FIle : main.py.py
# @Software : PyCharm

from mix_dataset import DatasetHandler, OutputType, DatasetType

if __name__ == "__main__":
    # 数据集所在的路径
    base_file_path = "dataset/gyafc_em"
    # 数据集对应的类型
    dataset_type = "valid"

    # 读取数据集的位置(偏移量)和大小
    size = -1
    # 运行程序
    handler = DatasetHandler(base_file_path, DatasetType.valid,
                             read_size=size,
                             output_type=OutputType.Json)
    handler.handle()
