import logging
from logging.handlers import TimedRotatingFileHandler

def server_log():
    log_level= logging.DEBUG

    logger = logging.getLogger("server_log")
    
    logger.setLevel(log_level)

    # 检查是否已经有处理器，避免重复添加
    if not logger.hasHandlers():
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

        # 设置后缀名称，跟strftime的格式一样
time    file_handler.suffix = "%Y-%m-%d_%H-%M-%S.log"
        formatter = logging.Formatter(
            "%(asctime)s | %(pathname)s | %(funcName)s | %(lineno)s | %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S")
        # 将格式器添加到处理器
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # 将处理器添加到记录器
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger
