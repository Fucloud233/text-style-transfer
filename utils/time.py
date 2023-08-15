# -*- coding = utf-8 -*-
# @Time : 2023/08/08 18:45
# @Autor : Fucloud
# @FIle : time.py
# @Software : PyCharm

from datetime import datetime


def get_log_file_time() -> str:
    log_file_fmt = "%Y-%m-%d %H-%M-%S"
    return __get_cur_time(log_file_fmt)


def get_log_time() -> str:
    log_fmt = "%H:%m:%S"
    return __get_cur_time(log_fmt)


def __get_cur_time(fmt: str) -> str:
    return datetime.now().strftime(fmt)


def get_cur_time() -> datetime:
    return datetime.now()


# 得到所需要所花费的时间
def get_need_time(begin_time: datetime) -> int:
    return (datetime.now() - begin_time).seconds


if __name__ == "__main__":
    print("cur_time: ", get_log_file_time())