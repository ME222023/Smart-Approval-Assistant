from utils import Config
from chat.wechat_client import WechatClient
qw = WechatClient()
redisurl = Config.redis_url

print(redisurl)

def shwo():
    # global redisurl, adminids
    
    # print(id(Config))
    # print(id(Config.redis_url), Config.redis_url)
    # print(id(redisurl), redisurl)
    print(Config.admin_ids)
    qw.send_text("DONE!!!", [Config.admin_ids])
    # print(type(Config.admin_ids))
    # print(Config.getNameIdList("17a755177f4ad1f1d99bf8042cfbb74a"))
    # list = Config.getNameList()
    # print(list)

