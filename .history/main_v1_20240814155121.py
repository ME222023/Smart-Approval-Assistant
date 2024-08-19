import logging
from test_v1 import adminApprove
from chat_server_v1 import re

# 管理员的id
admin_ids = [
    "17a755177f4ad1f1d99bf8042cfbb74a",
    "1730846d950e0a5709ac2ea44138df09"
]

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)  # 设置最低日志级别为DEBUG

# 创建一个日志处理器，输出到文件
file_handler = logging.FileHandler('my_log.log')
file_handler.setLevel(logging.DEBUG)

# 创建一个日志处理器，输出到控制台
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# 创建一个日志格式器
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s')

# 将格式器添加到处理器
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# 将处理器添加到记录器
logger.addHandler(file_handler)
logger.addHandler(console_handler)



    # client.flushdb()
while True:
    with RedisClient(redis_url="redis://:123@10.5.5.73:16379/v1") as client:
        keys = client.keys()
    logger.debug(f"从Redis中获取到的所有键: {keys}")
    for k in keys:
        k = k.decode("utf-8")
        if not k.startswith("msg_"):
            continue
        # 用户的id信息
        from_id = k.split("_")[-1]
        user_id = f"{from_id}"
        logger.debug(f"处理键 {k} 对应的用户ID: {user_id}")
        # 管理员审批
        if user_id in admin_ids:
            msg = client.lpop(k)
            msg = msg.decode("utf-8")
            adminApprove(user_id, msg)
        # 用户交互
        else:
            regular(k, user_id)


