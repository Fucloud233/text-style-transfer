from utils import time

class ScheduleLog:
    def __init__(self, with_start=False):
        self.__begin_time = None
        self.__is_start = False

        self.__pre_time = None
        
        # 自动开启计时
        if with_start:
            self.start()

    def start(self):
        if not self.__is_start:
            self.__begin_time = time.now()
            self.__is_start = True

            # init the pre_time after starting
            self.__pre_time = self.__begin_time
        else:
            raise RuntimeWarning("The sceduleLog has started!")
        

    def clear(self):
        self.__begin_time = None

    def log(self, info):
        print("[%02.2fs] %s" % (self.cur_time, info))

    def mark(self):
        self.__pre_time = time.now()

    @property
    def take_time(self):
        cur_time = time.now()
        return time.cal_time(self.__pre_time, cur_time)

    @property
    def cur_time(self):
        if self.__begin_time is None:
            return None

        return time.cal_time(self.__begin_time, time.now())
