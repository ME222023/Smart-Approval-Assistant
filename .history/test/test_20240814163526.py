import logging

# 创建一个logger对象
logger = logging.getLogger('my_logger')
logger.setLevel(logging.DEBUG)  # 设置日志级别为DEBUG

# 创建一个处理器，用于将日志输出到终端
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# 创建一个处理器，用于将日志写入文件
file_handler = logging.FileHandler('logfile.log')
file_handler.setLevel(logging.DEBUG)

# 创建一个格式化器，并将其添加到处理器中
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# 将处理器添加到logger对象中
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# 记录一些日志
logger.debug('This is a debug message')
logger.info('This is an info message')
logger.warning('This is a warning message')
logger.error('This is an error message')
logger.critical('This is a critical message')
