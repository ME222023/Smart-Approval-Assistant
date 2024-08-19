# -*- encoding:utf-8 -*-
import time
from xml.dom.minidom import parseString
from chat_tool import chat
from WXBizMsgCrypt3 import WXBizMsgCrypt  # 库地址 https://github.com/sbzhu/weworkapi_python
from prompt_hub import *

sToken = "vCTCmUX8BmCTuKFlAlMT"
sEncodingAESKey = "bJ84sa2wXyHrkHM6Vlw6PpO75jemC7FLphM4W89bBaU"
sReceiveId = "ww8da50fdd614a1fb6"
AgentId = 1000188
Secret = 'mJKa7u98-9Gv5i_Bp4A1gIR-KrKO9vsA6ziIfdJN_bg'
# 对应接受消息回调模式中的token，EncodingAESKey 和 企业信息中的企业id
org_api = WXBizMsgCrypt(sToken, sEncodingAESKey, sReceiveId)

# 测试
# sToken = "hJqcu3uJ9Tn2gXPmxx2w9kkCkCE2EPYo"
# sEncodingAESKey = "6qkdMrq68nTKduznJYO1A37W2oEgpkMUvkttRToqhUt"
# sCorpID = "ww1436e0e65a779aee"
# org_api = WXBizMsgCrypt(sToken, sEncodingAESKey, sCorpID)



# 开启消息接受模式时验证接口连通性
def signature(msg_signature, timestamp, nonce, echo_str):
    ret, sEchoStr = org_api.VerifyURL(msg_signature, timestamp, nonce, echo_str)
    if ret != 0:
        print("ERR: VerifyURL ret: " + str(ret))
        return "failed"
    else:
        return sEchoStr


# 实际接受消息
def signature2(msg_signature, timestamp, nonce, data):
    ret, sMsg = org_api.DecryptMsg(data, msg_signature, timestamp, nonce)
    if ret != 0:
        print("ERR: DecryptMsg ret: " + str(ret))
        return "failed", ""
    dom = parseString(sMsg)
    root = dom.documentElement
    print(f"request_decrypt_xml：\n {root.toprettyxml()}")
    type_xml = root.getElementsByTagName("MsgType")[0].childNodes[0].data
    return type_xml, sMsg


def extracte_info(sMsg, type_xml):
    dom = parseString(sMsg)
    root = dom.documentElement
    if type_xml == "text":
        result = root.getElementsByTagName("Content")[0].childNodes[0].data
    elif type_xml in ["image", "file"]:
        result = root.getElementsByTagName("MediaId")[0].childNodes[0].data
    else:
        result = ""
    from_user = root.getElementsByTagName("FromUserName")[0].childNodes[0].data
    msg_id = root.getElementsByTagName("MsgId")[0].childNodes[0].data
    return result, from_user, msg_id

PROMPT= """
作为一个很棒的调度系统审核AI助理, 你的任务是帮助用户审核调度任务，回答用户相关的问题

审核调度任务只需要提供调度id即可
"""

def generate_messages(instruction: str, sys_prompt:str):
    """生成请求的chats信息，匹配promot,func_des"""

    user_message = {
        "role": "user",
        "content": instruction
    }
    # user_message.update({"name": "xxxx_function"})
    messages = [
        {
            "role": "system",
            "content": sys_prompt
        },
        user_message
    ]
    return messages


def exception_handler(response):
    if "error" in response:
        return "模型请求失败，请稍后继续尝试"
    else:
        return response.get("content")


def step_gpt(messages: list, func=None):

    data = {
        "model": "gpt-4o", # gpt-3.5-turbo
        "messages": messages,
        "stream": False,
        "temperature": 0.2
    }
    if func is not None:
        data.update({"functions": [func]})
    ans = chat(data=data)
    return exception_handler(ans)


def repsone_gpt(chat_info, sys_prompt):
    message = generate_messages(chat_info, sys_prompt)
    content = step_gpt(message)
    return content


def generate_time():
    timestamp = time.time()
    return timestamp


# 回复消息
def encrypt_replying_messages(from_user, content, msgid, request_nonce, request_timestamp):
    rely_info = f"""<xml>
    <ToUserName><![CDATA[ww8da50fdd614a1fb6]]></ToUserName>
    <FromUserName><![CDATA[{from_user}]]></FromUserName>
    <CreateTime>1707203414</CreateTime>
    <MsgType><![CDATA[text]]></MsgType>
    <Content><![CDATA[{content}]]></Content>
    <MsgId>{msgid}</MsgId>
    <AgentID>1000188</AgentID>
    </xml>"""
    print(f"response xml: {rely_info}")
    ret, sEncryptMsg = org_api.EncryptMsg(rely_info, request_nonce, request_timestamp)
    if ret != 0:
        raise Exception("encrypt_replying_messages: 加密失败")
    return sEncryptMsg


def approval_process_message(querys):
    result = "审批列表如下（最多展示20条）：\n["
    for idx, row in enumerate(querys[:20]):
        _result = f"{row.task_id} : {row.task_name}/{row.applicant}"
        result = "\n".join([result, _result])
    result = "\n".join([result, "]", "回复“审批请求确认”: 默认全部审批请求校验分析开始",
                        "回复“审批请求确认 task_id”: 指定task_id审批请求校验分析开始",
                        "回复“审批请求确认包含**”: 指定包含**的task_names审批请求校验分析开始",
                        ])
    return result


if __name__ == '__main__':
    sql = "select event_day as event_day,cust_code as cust_code,account as account,djzj as djzj,zzj as zzj,jyzj as jyzj,remark as remark,timestamp_column as timestamp_column,'${yyyy-MM-dd}' as busi_date from INV_DM.TEST_TABLE"

    content = repsone_gpt(sql, sys_prompt=SYS_PROMPT_SQL)

    print

    # pass
    # import re
    # sMsg = "审批请求确认 1231 54654 789"
    # sMsg = "审批请求确认包含 asf"
    # a = re.match(r"审批请求确认(\s*\d+)+$", sMsg)
    # b = re.match(r"审批请求确认只包含(\w+)$", sMsg)
    # # a = re.search(r"^审批请求确认(?P<task_id>\s*\d+)+", "审批请求确认10515 10056 8841")
    # # print(a)
    # # print(a.group("task_id"))
    # print(b)
