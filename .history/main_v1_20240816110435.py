import os
import time
from utils.log_handle import server_log
from utils.redis_handle import RedisClient
from admin_interact import adminInteract
from cus_interact import cusInteract
from utils.config import Config
# 生成函数调用图像
from pycallgraph2 import PyCallGraph
from pycallgraph2.output import GraphvizOutput

config = Config()
config.init("/home/hezp1/AI/app_weichat/config.ini")

redis_url = config.config['server']['redis_url']
admin_ids = config.config['server']['admin_ids']

# 管理员的id
# admin_ids = [
#     "17a755177f4ad1f1d99bf8042cfbb74a",
#     "1730846d950e0a5709ac2ea44138df09"
# ]

logger = server_log()
# with RedisClient(redis_url="redis://:123@10.5.5.73:16379/v1") as client:
#     client.flushdb()

def main():
    graphviz = GraphvizOutput()
    graphviz.output_file = 'graph_mainv1_test.png'

    with PyCallGraph(output=graphviz):
        while True:
            with RedisClient(redis_url) as client:
                keys = client.keys()
            # logger.debug(f"从Redis中获取到的所有键: {keys}")
            for k in keys:
                print("2-------------------------------")
                k = k.decode("utf-8")
                if not k.startswith("msg_"):
                    continue
                # 用户的id信息
                print("22-------------------------------")
                from_id = k.split("_")[-1]
                user_id = f"{from_id}"
                logger.debug(f"处理键 {k} 对应的用户ID: {user_id}")
                # 管理员审批
                if user_id in admin_ids:
                    print("3-------------------------------")
                    with RedisClient(redis_url) as client:
                        msg = client.lpop(k)
                    print("4-------------------------------")
                    msg = msg.decode("utf-8")
                    adminInteract(user_id, msg)
                # 用户交互
                else:
                    print("5-------------------------------")
                    cusInteract(k, user_id)
            time.sleep(2)

if __name__ == '__main__':
    main()

