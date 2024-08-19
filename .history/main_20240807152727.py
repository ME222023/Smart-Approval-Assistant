from test import *
from chat_server import *

# 管理员的id
admin_ids = [
    "17a755177f4ad1f1d99bf8042cfbb74a"
]
admin = "|".join(admin_ids)

with RedisClient(redis_url="redis://:123@10.5.5.73:16379/v1") as client:
    while True:
        keys = client.keys()
        for k in keys:
            k = k.decode("utf-8")
            if not k.startswith("msg_"):
                continue
            # 用户的id信息
            from_id = k.split("_")[-1]
            user_id = f"{from_id}"
            # 管理员审批
            if user_id in admin_ids:
                msg = client.lpop(k)
                msg = msg.decode("utf-8")
                # print(msg)
                # print(type(msg))
                adminApprove(user_id, msg)
            # 用户交互
            else:
                regular(k, user_id)




