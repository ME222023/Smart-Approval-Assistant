import os
import time
import logging
from logging.handlers import TimedRotatingFileHandler
from utils.redis_handle import RedisClient
from test_v1 import adminApprove
from chat_server_v1 import regular

# 管理员的id
admin_ids = [
    "17a755177f4ad1f1d99bf8042cfbb74a",
    "1730846d950e0a5709ac2ea44138df09"
]
if not os.path.exists("server_logs"):
    os.makedirs("server_logs")

logger = logging.getLogger()
log_level= logging.DEBUG

# 创建一个日志处理器，输出到文件，日志文件按日分割
file_handler = TimedRotatingFileHandler(
    "server_logs/server.log",  # 日志路径
    when='D',  # S秒 M分 H时 D天 W周 按时间切割 测试选用S
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


# client.flushdb()
# while True:
#     with RedisClient(redis_url="redis://:123@10.5.5.73:16379/v1") as client:
#         keys = client.keys()
#     logger.debug(f"从Redis中获取到的所有键: {keys}")
#     for k in keys:
#         k = k.decode("utf-8")
#         if not k.startswith("msg_"):
#             continue
#         # 用户的id信息
#         from_id = k.split("_")[-1]
#         user_id = f"{from_id}"
#         logger.debug(f"处理键 {k} 对应的用户ID: {user_id}")
#         # 管理员审批
#         if user_id in admin_ids:
#             msg = client.lpop(k)
#             msg = msg.decode("utf-8")
#             adminApprove(user_id, msg)
#         # 用户交互
#         else:
#             regular(k, user_id)
#     time.sleep(1)


