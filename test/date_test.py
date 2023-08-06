# -*- coding = utf-8 -*-
# @Time : 2023/07/29 22:57
# @Autor : Fucloud
# @FIle : date_test.py
# @Software : PyCharm

from datetime import date
from datetime import datetime

record_day = 3


# 确定日期是否有效
def is_valid_date(input_date_str: str):
    input_date = datetime.strptime(input_date_str, '%Y-%m-%d')
    sub_result = (datetime.now() - input_date).days.real

    return sub_result < record_day


def date_sub_test():
    # 根据字符串来获得时间
    str_p = '2019-01-30'
    date_p = datetime.strptime(str_p, '%Y-%m-%d').date()
    print(date_p, type(date_p))  # 2019-01-30 <class 'datetime.date'>

    # 根据结构化数据获得时间
    before_date_p = date(2019, 1, 29)
    print("before date", before_date_p)

    # 时间减法
    date2_p = date_p - before_date_p
    print("sub result: ", date2_p)

    # 转换为日期
    result = date2_p.days.real
    print("int result: {}, type: {}".format(result, type(result)))


if __name__ == "__main__":
    date_sub_test()