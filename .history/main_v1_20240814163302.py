import os
import time

from utils.log_handle import server_log
from utils.redis_handle import RedisClient
# from test_v1 import adminApprove
# from chat_server_v1 import regular

# 管理员的id
admin_ids = [
    "17a755177f4ad1f1d99bf8042cfbb74a",
    "1730846d950e0a5709ac2ea44138df09"
]

logger = server_log()
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


