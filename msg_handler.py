import os
import time


from utils.log_handle import server_log
from redis_handler.redis_handle import RedisClient
from interaction_handler.admin_interact_handle import admin_interact
from interaction_handler.cus_interact_handle import cus_interact
from utils.config import Config
# 生成函数调用图像
from pycallgraph2 import PyCallGraph
from pycallgraph2.output import GraphvizOutput

logger = server_log()
# with RedisClient(redis_url="redis://:123@10.5.5.73:16379/v1") as client:
#     client.flushdb()
# -----------------------绘制函数调用图像---------------------------------------------------
def main():
    graphviz = GraphvizOutput()
    graphviz.output_file = 'schedule_graph.png'

    with PyCallGraph(output=graphviz):
        while True:
            with RedisClient(Config.redis_url) as client:
                keys = client.keys()
            # logger.debug(f"从Redis中获取到的所有键: {keys}")
            for k in keys:
                k = k.decode("utf-8")
                if not k.startswith("msg_"):
                    continue
                # 用户的id信息
                from_id = k.split("_")[-1]
                user_id = f"{from_id}"
                logger.debug(f"处理键 {k} 对应的用户ID: {user_id}")
                # 管理员审批
                if user_id in Config.admin_ids:
                    with RedisClient(Config.redis_url) as client:
                        msg = client.lpop(k)
                    msg = msg.decode("utf-8")
                    admin_interact(user_id, msg)
                # 用户交互
                else:
                    cus_interact(k, user_id)
            time.sleep(2)

if __name__ == '__main__':
    main()
# ----------------------------------------------------------------------

# 重新启动清空redis队列
# with RedisClient(Config.redis_url) as client:
#     client.flushall()

# while True:
#     with RedisClient(Config.redis_url) as client:
#         keys = client.keys()
#     for k in keys:
#         k = k.decode("utf-8")
#         if not k.startswith("msg_"):
#             continue
#         # 提取发送消息者ID信息
#         from_id = k.split("_")[-1]
#         user_id = f"{from_id}"
#         logger.debug(f"处理键 {k} 对应的用户ID: {user_id}")
#         # 管理员和小智交互的相关操作
#         if user_id in Config.admin_ids:
#             with RedisClient(Config.redis_url) as client:
#                 msg = client.lpop(k)
#             msg = msg.decode("utf-8")
#             admin_interact(user_id, msg)
#         # 用户和小智交互的相关操作
#         else:
#             cus_interact(k, user_id)
#     time.sleep(2)

