# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

"""
Refer
* https://blog.csdn.net/weixin_43750377/article/details/103855911
"""

# useful for handling different item types with a single interface
import csv
from pathlib import Path


class YangshiproPipeline:
    def __init__(self):
        self.output_path = Path("output")
        self.output_file_name = "yangshi_news"
        self.file_suffix = "csv"
        self.file_handler_list = {}

        # 设置文件第一行的字段名，注意要跟spider传过来的字典key名称相同
        self.fieldnames = ["id",
                           "timeline",
                           "title",
                           "category",
                           "keywords",
                           "origin",
                           "image",
                           "focus_date",
                           "brief",
                           "url",
                           "image2",
                           "content",
                           "image3",
                           "count",
                           "ext_field"
                           ]

    '''
        重写父类方法
        该仅仅在爬虫开始时调用一次
    '''

    def open_spider(self, spider):
        pass

    def check_file(self, category: str):
        if category in self.file_handler_list:
            return

        # 生成文件名
        def get_file_name() -> Path:
            file_name = f"{self.output_file_name}_{category}.{self.file_suffix}"
            return Path.joinpath(self.output_path, file_name)

        if not self.output_path.exists():
            self.output_path.mkdir()

        # 打开文件，指定方式为写，newlines="" 消除产生的空行
        cur_file = open(get_file_name(), 'a', newline='', encoding='utf-8')
        # 指定文件的写入方式为csv字典写入，参数1为指定具体文件，参数2为指定字段名
        cur_writer = csv.DictWriter(cur_file, fieldnames=self.fieldnames)
        # 写入第一行字段名
        cur_writer.writeheader()

        self.file_handler_list[category] = {
            "file": cur_file,
            "writer": cur_writer
        }

    def process_item(self, item, spider):
        cur_category = item['category']
        # 验证文件是否存在
        self.check_file(cur_category)
        # 写入数据
        self.file_handler_list[cur_category]["writer"].writerow(item)
        print('保存成功', item['category'], item['title'])
        return item  # 传递给下一个执行的管道类

    def close_spider(self, spider):
        # [注意] 遍历values集合
        for handler in self.file_handler_list.values():
            handler["file"].close()
        print('结束爬虫...')
