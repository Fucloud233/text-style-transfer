from utils import time

class ScheduleLog:
    def __init__(self, with_start=False):
        self.__begin_time = None
        self.__is_start = False
        
        # 自动开启计时
        if with_start:
            self.start()

    def start(self):
        if not self.__is_start:
            self.__begin_time = time.now()
            self.__is_start = True
        else:
            raise RuntimeWarning("The sceduleLog has started!")
        

    def clear(self):
        self.__begin_time = None

    def log(self, info):
        print("[%02.2fs] %s" % (self.cur_time, info))

    @property
    def cur_time(self):
        if self.__begin_time is None:
            return None

        return time.cal_time(self.__begin_time, time.now())
