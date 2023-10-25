from datetime import datetime

def now():
    return datetime.now()

def cal_time(begin: datetime, end: datetime):
    delta_time = end - begin
    return delta_time.seconds + delta_time.microseconds / 1000000