import logging
from logging.handlers import TimedRotatingFileHandler


def _server_log_func():
    logger = logging.getLogger("server_log")
    log_level= logging.DEBUG

    # 创建一个日志处理器，输出到文件，日志文件按日分割
    file_handler = TimedRotatingFileHandler(
        "server_logs/server.log",  # 日志路径
        when='D',  # S秒 M分 H时 D天 W周 按时间切割
        encoding='utf-8'
    )
    # file_handler.suffix = "%Y-%m-%d_%H-%M-%S.log"
    file_handler.setLevel(log_level)

    # 创建一个日志处理器，输出到控制台
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)

    # 创建一个日志格式器
    formatter = logging.Formatter(
        "%(asctime)s | %(pathname)s | %(funcName)s | %(lineno)s | %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S")
    # 将格式器添加到处理器
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # 将处理器添加到记录器
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logger.info(f"从Redis中获取到的所有键")

    return logger

def _server_log_func():