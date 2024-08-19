import random

import uvicorn
import os
import re
import time
import logging.handlers
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from message_hander import signature, signature2, repsone_gpt, encrypt_replying_messages, extracte_info, approval_process_message
from send_app import qywx
from chat_tool import chat
from message_hander import step_gpt, generate_messages
from task_approval import task_info, by_task_id

from prompt_hub import *
# from mysql.crud import get_task_info_by_applicant, modify_approval_result
# from mysql.database import SessionLocal

# mysql = SessionLocal()

app = FastAPI()
qy = qywx()

# Config logs file
if not os.path.exists("static"):
    os.makedirs("static")
# Config logs file
if not os.path.exists("logs"):
    os.makedirs("logs")
# ################生产要修改#####################
log_level = logging.DEBUG
# #######################################
logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(log_level)
# 添加TimedRotatingFileHandler
timefilehandler = logging.handlers.TimedRotatingFileHandler(
    "logs/weichat.log",  # 日志路径
    when='D',  # S秒 M分 H时 D天 W周 按时间切割 测试选用S
    encoding='utf-8'
)
# 设置后缀名称，跟strftime的格式一样
timefilehandler.suffix = "%Y-%m-%d_%H-%M-%S.log"
formatter = logging.Formatter(
    "%(asctime)s | %(pathname)s | %(funcName)s | %(lineno)s | %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S")
timefilehandler.setFormatter(formatter)
logger.addHandler(timefilehandler)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)

users = {
    'admin': "17a755177f4ad1f1d99bf8042cfbb74a",
    "cus": "1730846d950e0a5709ac2ea44138df09"
}

@app.get("/")
def index():
    return "welcome to navigation fastapi"


@app.get("/weichat")
def get_weichat(request: Request):
    msg_signature = request.query_params.get("msg_signature")
    timestamp = request.query_params.get("timestamp")
    nonce = request.query_params.get("nonce")
    echostr = request.query_params.get("echostr", )
    sEchoStr = signature(msg_signature, timestamp, nonce, echostr)
    if sEchoStr == "failed":
        return "get_weichat: 解密失败"
    else:
        echo_str = int(sEchoStr.decode("utf-8").replace("\"","").replace("\n", ""))
        return echo_str


@app.post("/weichat")
async def post_weichat(request: Request):
    logger.info(f"request_url: {request.url}")
    msg_signature = request.query_params.get("msg_signature")
    timestamp = request.query_params.get("timestamp")
    nonce = request.query_params.get("nonce")
    request_body = await request.body()
    data = request_body.decode("utf-8")
    logger.info(f"request_body: {data}")
    type_xml, sMsg = signature2(msg_signature, timestamp, nonce, data)
    content, from_user, msg_id = extracte_info(sMsg, type_xml)
    logger.info(f"content: {content}, from_user: {from_user}, msg_id: {msg_id}")
    logger.info(f"type_xml: {type_xml}, sMsg: {sMsg}")
    # TODO: 测试用的
    oa_account = "guoyf2"
    if type_xml == "failed":
        return encrypt_replying_messages(from_user, "signature2解密失败，请上报给管理者", msg_id, nonce, timestamp)
    elif type_xml == "text":
        print("-------------content:", content)
        # numbers = re.findall(r'\d+', content)
        # sql = "select event_day as event_day,cust_code as cust_code,account as account,djzj as djzj,zzj as zzj,jyzj as jyzj,remark as remark,timestamp_column as timestamp_column,'${yyyy-MM-dd}' as busi_date from INV_DM.TEST_TABLE"
        #     # list(map(int, re.findall(r'\d+', content)))
            
        # if "优化" in content:
        #     qy.send_text(f'稍等，我正在帮助你分析sql', [f'{from_user}'])
        #     # content = repsone_gpt(sql, sys_prompt=SYS_PROMPT_SQL)
        #     # print(content)
        #     time.sleep(5)
        #     content = f"{sql} \n 语法上没有明显错误，字段名和表名都正确引用\n你在SELECT子句中为每个字段都指定了别名，但这些别名与原字段名相同，这样做没有实际意义。可以直接使用字段名，而不需要重复指定别名。"
        #     return encrypt_replying_messages(from_user, content, msg_id, nonce, timestamp)
        
        # if "拒绝" in content or "不通过" in content:
        #     # for t in numbers:
        #     #     by_task_id(t, approval=False)
        #     if from_user == users['admin']:
        #         u = users['cus']
            
        #         qy.send_text(f'管理员拒绝了你的请求，请联系管理员', [f'{u}'])
        #     else:
        #         return encrypt_replying_messages(from_user, '非管理员无审批权限', msg_id, nonce, timestamp)
        # elif "通过" in content or "批准" in content:
        #     # for t in numbers:
        #     #     by_task_id(t)
        #     if from_user == users['admin']:
        #         u = users['cus']
        #         qy.send_text(f'管理员通过了你的请求', [f'{u}'])
        #     else:
        #         return encrypt_replying_messages(from_user, '非管理员无审批权限', msg_id, nonce, timestamp)
        # if len(numbers) > 0:
        #     print("-------------numbers", numbers)
        #     l_str = "、".join(numbers)
        #     u= users["admin"]
        #     qy.send_text(f'任务 {l_str} 等待审批！', [f'{u}'])
        #     time.sleep(3)
        #     qy.send_text(f'正在检查任务', [f'{from_user}'])
        #     time.sleep(3)
        #     return encrypt_replying_messages(from_user, '已提交管理员', msg_id, nonce, timestamp)
        # content = repsone_gpt(content, sys_prompt=SYS_PROMPT_DEFAULT)
        # return encrypt_replying_messages(from_user, content, msg_id, nonce, timestamp)
    elif type_xml in ["file", "image"]:
        media_id = content
        res = qy.download_file(media_id)
        logger.info(f"download file log: {res}")
        return encrypt_replying_messages(from_user, f"暂时只支持文本回复{type_xml}", msg_id, nonce, timestamp)
        # TODO: 功能后续处理
    else:
        return encrypt_replying_messages(sMsg,"暂时只支持文本回复", msg_id, nonce, timestamp)


if __name__ == "__main__":
    import os
    PORT = os.getenv("PORT")
    WORKERS = os.getenv("WORKERS")
    PORT = 10051
    WORKERS = 2
    assert PORT is not None
    assert WORKERS is not None
    uvicorn.run("web_api:app", host='0.0.0.0', log_level="debug", reload=True, port=int(PORT), workers=int(WORKERS))

