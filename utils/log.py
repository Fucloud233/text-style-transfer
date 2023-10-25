from utils import time

class ScheduleLog:
    def __init__(self):
        self.__begin_time = None

    def start(self):
        self.__begin_time = time.now()

    def clear(self):
        self.__begin_time = None

    def log(self, info):
        print("[%2.3fs] %s" % (self.cur_time, info))

    @property
    def cur_time(self):
        if self.__begin_time is None:
            return None

        return time.cal_time(self.__begin_time, time.now())
