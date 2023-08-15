# -*- coding = utf-8 -*-
# @Time : 2023/08/08 18:44
# @Autor : Fucloud
# @FIle : log.py
# @Software : PyCharm

from enum import Enum
from pathlib import Path
from utils import time


class LogType(Enum):
    info = 'info'
    warn = 'warn'
    error = 'error'
    debug = 'debug'

    def __str__(self):
        return self.name


class Log:
    __output_path = Path("log")
    __log_file = None
    __show_on_cli = True
    __show_on_file = False
    # 日志文件收集时长(s)
    __collect_time = 5 * 60
    __cur_time = time.get_cur_time()

    # 静态函数初始化
    @staticmethod
    def init(show_on_cli: bool = True, show_on_file: bool = False):
        if show_on_file:
            Log.__create()
        Log.show_on_cli = show_on_cli
        Log.__show_on_file = show_on_file

    # 创建log文件
    @staticmethod
    def __create():
        try:
            if not Log.__output_path.exists():
                Log.__output_path.mkdir()

            # 创建文件
            log_file_name = Path(Log.__get_log_file_name())
            log_file_name = Path.joinpath(Log.__output_path, log_file_name)
            Log.__log_file = open(log_file_name, "a", encoding="utf-8")
        except Exception:
            Log.__log(LogType.error, "Log文件创建失败")

    @staticmethod
    def __check_valid() -> bool:
        return Log.__log_file is not None

    @staticmethod
    def __log(msg_type: LogType, *args):
        # 生成文本
        raw_log_msg = ""
        for arg in args:
            raw_log_msg += str(arg) + ' '

        log_msg = Log.__gen_log_msg(msg_type, raw_log_msg)
        if Log.__show_on_cli:
            print(log_msg, end="")
        if Log.__show_on_file and Log.__check_valid():
            Log.__log_file.write(log_msg)

    # 生成日志信息
    @staticmethod
    def __gen_log_msg(msg_type: LogType, msg: str) -> str:
        return "[%s]%-7s %s\n" % (time.get_log_time(), f"[{msg_type}]", msg)

    @staticmethod
    def __get_log_file_name() -> str:
        # log_time_name: str
        #
        # # 计算两次Log收集时间是否相隔大于收集时间
        # # 如果大于则创建新文件
        # delta_time = Log.__cur_time - time.get_cur_time()
        #
        # Log.debug("delta_time", delta_time)
        # if delta_time.seconds > Log.__collect_time:
        #     Log.__cur_time = time.get_cur_time()
        return time.get_log_file_time() + ".log"

    # 清除所有日志文件
    @staticmethod
    def clear():
        if not Log.__output_path.exists():
            return
        # 删除文件
        for file in Log.__output_path.iterdir():
            file.unlink()

    @staticmethod
    def info( *args):
        Log.__log(LogType.info, *args)

    @staticmethod
    def warn(*args):
        Log.__log(LogType.warn, *args)

    @staticmethod
    def error(*args):
        Log.__log(LogType.error, *args)

    @staticmethod
    def debug(*args):
        Log.__log(LogType.debug, *args)


if __name__ == "__main__":
    Log.clear()
    Log.init()
    Log.info("hello", 1, 2, 3)
    Log.error("file not found")
    Log.warn("you are wrong")
