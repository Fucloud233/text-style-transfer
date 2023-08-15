# -*- coding = utf-8 -*-
# @Time : 2023/08/06 17:51
# @Autor : Fucloud
# @FIle : bilibili_html_parser.py
# @Software : PyCharm

# refer: https://zhuanlan.zhihu.com/p/135867579

from collections.abc import MutableMapping
from lxml import etree
from datetime import date
import datetime
from pathlib import Path
import csv


def get_real_date(date_text: str) -> date:
    date_text = date_text.strip()[2:]

    if "分钟前" in date_text or "小时前" in date_text:
        return date.today()
    elif date_text == "昨天":
        # 计算昨天日期
        # https://www.runoob.com/python3/python3-get-yesterday.html
        return date.today() + datetime.timedelta(-1)

    dates = date_text.split("-")
    if len(dates) == 3:
        return datetime.datetime.strptime(date_text, "%Y-%m-%d").date()
    elif len(dates) == 2:
        month, day = int(dates[0]), int(dates[1])
        return datetime.date(date.today().year, month, day)


def get_id(url_string: str) -> str:
    return url_string.split('/')[-2]


class Item:
    __field_names = ['id', 'url', 'title', 'author', 'publish_date']

    def __init__(self, id: str, url: str, title: str, author: str, publish_date: date):
        self.__map = {
            'id': id, 'url': url, 'title': title, "author": author, 'publish_date': publish_date
        }

    def __str__(self) -> str:
        return f"title: {self.__map['title']} by {self.__map['author']} at {self.__map['publish_date']}"

    @staticmethod
    def get_field_names() -> list[str]:
        return Item.__field_names

    def get_map(self) -> dict[str, any]:
        return self.__map


class HTMLParser:
    url_xpath = '//*[@class="bili-video-card__wrap __scale-wrap"]/a/@href'
    title_xpath = '//*[@class="bili-video-card__info--tit"]/a/text()'
    author_xpath = '//*[@class="bili-video-card__info--author"]/text()'
    date_xpath = '//*[@class="bili-video-card__info--date"]/text()'

    html_data = None
    result_items: list[Item]

    def __init__(self):
        pass

    # 读取html文件
    def read_html(self, input_html_file_path: str):
        with open(input_html_file_path, "r", encoding="utf-8") as f:
            read_lines = f.readlines()
        # 整理html文件
        self.html_data = ""
        for line in read_lines:
            self.html_data += line.strip() + "\n"

    def parse(self):
        # 使用etree库进行解析
        xpath_data = etree.HTML(self.html_data)
        # 使用xpath语法解析
        urls = xpath_data.xpath(self.url_xpath)
        titles = xpath_data.xpath(self.title_xpath)
        authors = xpath_data.xpath(self.author_xpath)
        dates = xpath_data.xpath(self.date_xpath)

        self.result_items = []
        count = 0
        for i in range(len(urls)):
            try:
                item = Item(get_id(urls[i]), urls[i], titles[i],
                            authors[i], get_real_date(dates[i]))
                self.result_items.append(item)
            except IndexError:
                break

            count += 1

        print("[info] 解析完成, 共{}个视频".format(count))

    def save(self, output_file_path: str):
        file_path = Path(output_file_path)
        if not file_path.parent.exists():
            file_path.parent.mkdir()

        cur_file = open(output_file_path, 'w', newline='', encoding='utf-8')
        # 指定文件的写入方式为csv字典写入，参数1为指定具体文件，参数2为指定字段名
        cur_writer = csv.DictWriter(cur_file, fieldnames=Item.get_field_names())
        # 写入第一行字段名
        cur_writer.writeheader()

        for item in self.result_items:
            cur_writer.writerow(item.get_map())

        print("[info] 保存成功")


def main():
    input_file_name = "input/vlog.html"
    output_file_path = "output/vlog.csv"

    parser = HTMLParser()
    parser.read_html(input_file_name)
    parser.parse()
    parser.save(output_file_path)


if __name__ == "__main__":
    main()
