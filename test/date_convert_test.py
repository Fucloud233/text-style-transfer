# -*- coding = utf-8 -*-
# @Time : 2023/08/05 18:42
# @Autor : Fucloud
# @FIle : date_convert_test.py
# @Software : PyCharm

from datetime import date
import datetime


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


def convert(date_texts: list[str]) -> list[date]:
    result = []

    for text in date_texts:
        result.append(get_real_date(text))

    return result


def read_file(input_file_path: str) -> list[str]:
    with open(input_file_path, "r", encoding="utf-8") as f:
        source_texts = f.readlines()

    for i in range(len(source_texts)):
        source_texts[i] = source_texts[i].strip()

    return source_texts


def save_date_texts(
        output_file_path: str,
        source_texts: list[str],
        target_texts: list[date]
) -> None:
    length = len(source_texts)
    with open(output_file_path, "w", encoding="utf-8") as f:
        for i in range(length):
            if target_texts[i] is None:
                continue

            output_text = "{} -> {}\n".format(source_texts[i], target_texts[i])
            f.write(output_text)


if __name__ == "__main__":
    input_path = "input/date_input.txt"
    output_path = "output/date_output.txt"

    texts = read_file(input_path)
    print("read over")
    result_texts = convert(texts)
    print("convert over")
    save_date_texts(output_path, texts, result_texts)
    print("save over")

