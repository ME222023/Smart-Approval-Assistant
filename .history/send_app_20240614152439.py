# -*- encoding:utf-8 -*-
import requests
import json
import time
import os
from requests_toolbelt import MultipartEncoder

cur_path = os.path.dirname(os.path.abspath(__file__))

# AgentId：1000188
# Secret：mJKa7u98-9Gv5i_Bp4A1gIR-KrKO9vsA6ziIfdJN_bg
# CorpId：ww8da50fdd614a1fb6
# wxw-sit.axzq.com.cn
# wxw-sit.axzq.com.cn  企业微信
# 10.5.31.18，域名是wxw-sit.axzq.com.cn

class qywx:
    corpid = 'ww8da50fdd614a1fb6'  # 步骤1-3中的企业id
    # 此处将步骤1-2中的AgentId 和 Secret分别填入,多个应用逗号隔开
    app = (1000188, 'mJKa7u98-9Gv5i_Bp4A1gIR-KrKO9vsA6ziIfdJN_bg')

    def __init__(self):  # app_id 按app顺序编号
        self.agentid, self.corpsecret = qywx.app
        self.access_token = {'token': 'GoyXqeODnx_4lZvjF3ukoeMuv88r_soE-C4AgrzjJRkmQ5oGND6reSSc7Hac9Hsd-UzEEAmwhKGGIz0xpJzvMJ5m4E1EswR9Iz4yjgc0ER34cVQNSo2U6hLUD4kGxydxEc2uPlFwBeQrmxScezea6OOeMEV4HZBizZGR8kmkceNinPFCw2nublnURKp8OuMfGumYXImsz1rzs-WV8I1iakJ8lZ4zNgJuZ79EEtoI7Lw', 'expires': 1707276280}

    def get_access_token(self):
        if self.access_token and self.access_token["expires"] - 60 > int(time.time()):
            return self.access_token["token"]
        else:
            response = requests.get(
                "https://wxw-sit.axzq.com.cn/cgi-bin/gettoken?corpid={corpid}&corpsecret={corpsecret}".format(
                    corpid=qywx.corpid, corpsecret=self.corpsecret))
            data = json.loads(response.text)
            access_token = data['access_token']
            self.access_token = {"token": access_token, "expires": int(time.time()) + data["expires_in"]}
            print("access_token:", self.access_token)
            return access_token


    # 上传临时文件素材接口,图片也可使用此接口,20M上限, 该media_id仅3天内有效
    def post_file(self, filepath, filename):
        post_file_url = "https://wxw-sit.axzq.com.cn/cgi-bin/media/upload?access_token={access_token}&type=file".format(
            access_token=self.get_access_token())

        m = MultipartEncoder(
            fields={'file': (filename, open(filepath + filename, 'rb'), 'multipart/form-data')},
        )

        r = requests.post(url=post_file_url, data=m, headers={'Content-Type': m.content_type})
        js = json.loads(r.text)
        print(js)
        print("upload " + js['errmsg'])
        print("media", js['media_id'])
        if js['errmsg'] != 'ok':
            return None
        return js['media_id']

    # 向应用发送图片接口,_message为上传临时素材后返回的media_id
    def send_img(self, _message, useridlist=['name1|name2']):
        useridstr = "|".join(useridlist)

        json_dict = {
            "touser": useridstr,
            "msgtype": "image",
            "agentid": self.agentid,
            "image": {
                "media_id": _message,
            },
            "safe": 0,
            "enable_id_trans": 1,
            "enable_duplicate_check": 0,
            "duplicate_check_interval": 1800
        }
        json_str = json.dumps(json_dict)
        response_send = requests.post(
            "https://wxw-sit.axzq.com.cn/cgi-bin/message/send?access_token={access_token}".format(
                access_token=self.get_access_token()), data=json_str)
        print("send to " + useridstr + ' ' + json.loads(response_send.text)['errmsg'])
        return json.loads(response_send.text)['errmsg'] == 'ok'

    # 向应用发送文字消息接口,_message为字符串
    def send_text(self, _message, useridlist=['name1|name2']):
        useridstr = "|".join(useridlist)  # userid 在企业微信-通讯录-成员-账号
        json_dict = {
            "touser": useridstr,
            "msgtype": "text",
            "agentid": self.agentid,
            "text": {
                # text参数的content字段可以支持换行、以及A标签，即可打开自定义的网页
                # "你的快递已到，请携带工卡前往邮件中心领取。<br>出发前可查看<a href=\"https://wxw-sit.axzq.com.cn\">邮件中心视频实况</a>，聪明避开排队。"
                "content": _message
            },
            "safe": 0,
            "enable_id_trans": 1,
            "enable_duplicate_check": 0,
            "duplicate_check_interval": 1800
        }
        json_str = json.dumps(json_dict)
        print("urls    https://wxw-sit.axzq.com.cn/cgi-bin/message/send")
        response_send = requests.post(
            "https://wxw-sit.axzq.com.cn/cgi-bin/message/send?access_token={access_token}".format(
                access_token=self.get_access_token()), data=json_str)
        print("send to " + useridstr + ' ' + json.loads(response_send.text)['errmsg'])
        print(response_send.text)
        return json.loads(response_send.text)['errmsg'] == 'ok'



    # 向应用发送文档接口,_message为字符串
    def send_file(self, _message, useridlist=['name1|name2']):
        useridstr = "|".join(useridlist)  # userid 在企业微信-通讯录-成员-账号
        json_dict = {
            "touser": useridstr,
            "msgtype": "file",
            "agentid": self.agentid,
            "file": {
                "media_id": _message
            },
            "safe": 0,
            "enable_id_trans": 1,
            "enable_duplicate_check": 0,
            "duplicate_check_interval": 1800
        }
        json_str = json.dumps(json_dict)
        response_send = requests.post(
            "https://wxw-sit.axzq.com.cn/cgi-bin/message/send?access_token={access_token}".format(
                access_token=self.get_access_token()), data=json_str)
        print("send to " + useridstr + ' ' + json.loads(response_send.text)['errmsg'])
        print(response_send.text)
        return json.loads(response_send.text)['errmsg'] == 'ok'


    def group_recall_message(self, jobid):
        json_dict = {
            "jobid": jobid
        }
        json_str = json.dumps(json_dict)
        response_send = requests.post(
            "https://wxw-sit.axzq.com.cn/cgi-bin/appchat/revoke?access_token={access_token}".format(
                access_token=self.get_access_token()), data=json_str)
        print(response_send.text)
        print("group_recall_message" + jobid + ' ' + json.loads(response_send.text)['errmsg'])
        return json.loads(response_send.text)['errmsg'] == 'ok'


    def download_file(self, media_id):
        """
        通过media_id把文件（图片，文档）下载到本地
        :param media_id: 上传文件后可以获取
        :return:
        """
        res = requests.get(
            "https://wxw-sit.axzq.com.cn/cgi-bin/media/get?access_token={access_token}&media_id={media_id}".format(
                access_token=self.get_access_token(), media_id=media_id))
        file_name = res.headers.get("Content-Disposition", "").replace("attachment; filename=\"","")[:-1]
        print
        if res.status_code == 200 and res.headers.get("Error-Code") == "0":
            with open(f"{cur_path}/static/{file_name}", 'wb') as f:
                f.write(res.content)
        else:
            print(res.headers)
            return "download file fail"
        return "download file ok"



    def create_group(self, group_name, owner, userlist: list, chatid=""):
        json_dict = {
                "name": group_name,
                "owner": owner,
                "userlist": userlist,
                "chatid": chatid
                }
        json_str = json.dumps(json_dict)
        response = requests.post(
            "https://wxw-sit.axzq.com.cn/cgi-bin/appchat/create?access_token={access_token}".format(
                access_token=self.get_access_token()),  data=json_str)
        res = json.loads(response.text)
        print(res)
        print("create_group" + res["chatid"] + ' ' + res['errmsg'])
        return res['errmsg'] == 'ok'

    def group_info(self, chatid):
        response = requests.get(
            f"https://wxw-sit.axzq.com.cn/cgi-bin/appchat/get?access_token={self.get_access_token()}&chatid={chatid}")
        res = json.loads(response.text)
        print(res)

    def group_send_msg(self, chatid, msgtype, info):
        json_dict = {
            "chatid": chatid,
            "msgtype": msgtype,
            "text": {},
            "image": {},
            "voice": {},
            "video": {},
            "file": {},
            "textcard": {},
            "news": {},
            "mpnews": {}
        }
        json_dict.update({msgtype: info})
        json_str = json.dumps(json_dict)
        res = requests.post(
            f"https://wxw-sit.axzq.com.cn/cgi-bin/appchat/send?access_token={self.get_access_token()}", data=json_str)
        res = json.loads(res.text)
        print(res)

    def replace_forbid_words(self, media_id):
        json_dict = {
                "media_id": media_id}
        json_str = json.dumps(json_dict)
        res = requests.post(
            f"https://wxw-sit.axzq.com.cn/cgi-bin/corp/replace_forbid_words?access_token={self.get_access_token()}", data=json_str)
        res = json.loads(res.text)
        print(res)


    def get_oa_account(self, userid):
        response = requests.get(
            "https://wxw-sit.axzq.com.cn/cgi-bin/user/get?access_token={access_token}&userid={userid}".format(
                access_token=self.get_access_token(), userid=userid))
        res = json.loads(response.text)
        print(res)
        return res.get("english_name")


# 调用示例
if __name__ == '__main__':
    qy = qywx()
    # 发送文本消息
    qy.send_text('我是小钢', ['17a755177f4ad1f1d99bf8042cfbb74a'])
#     qy.send_text("""审批列表如下（最多展示20条）：
# [
# 10002784 : dm_risk_dmb_tyotc_inc_swap_contract/zhangzh4
# ]
# 回复“审批请求确认” 默认全部请求开始分析
# 回复“审批请求确认task_id” 指定请求开始分析""", ['17a755177f4ad1f1d99bf8042cfbb74a'])

    # 获取成员详情信息
    # qy.get_oa_account("17a755177f4ad1f1d99bf8042cfbb74a")

    # 发送图片消息, 需先上传至临时素材
    # media_id = qy.post_file('./', '6816733022841065111.jpg')
    # media_id = qy.post_file('./', '111.txt')

    # 111.txt :
    # txt_media_id = "16F2fn_-6ZmwnKf1YMnro7EcMmVxAk2uSoIdqiCTxb5yiMYYhPhrJmQsF-GSGp-z6"
    # qy.send_file(txt_media_id, ['17a755177f4ad1f1d99bf8042cfbb74a'])

    # 6816733022841065111.jpg:
    # pic_media_id = "1X0fE0VwakTNduMBQvpZRwedVcQtV_D_4up44ve9dpvXyYIaHGsaxAQcWZ0fT96A8"
    # qy.send_img(pic_media_id, ['17a755177f4ad1f1d99bf8042cfbb74a'])

    # 测试撤回信息
    # jobid = "4_1707214669_741821"
    # qy.group_recall_message(jobid)

    # 创建群聊
    # 'chatid': 'MTk3MDMyNDk2NjQ3MDYwMYsPvSxcmXkJ_ckaMz26bFw'
    # qy.create_group("小智助手测试群", "17a755177f4ad1f1d99bf8042cfbb74a", ["17a755177f4ad1f1d99bf8042cfbb74a", "1730846d950e0a5709ac2ea44138df09"], "1qaz2wsx3edc123456")

    # 下载文件内容
    # qy.download_file("1bbVLoOUKKJi6gEhCmjKynPmSSfp82CvF-OV0FNjV3m4c1pO-wjApnG4LpUPEX69u")

    # 查寻群组id为1qaz2wsx3edc123456的群信息
    # qy.group_info("1qaz2wsx3edc123456")

    # 向群组内传信息
    # qy.group_send_msg("1qaz2wsx3edc123456", "text", {"content": "各位大家并不好"})
    # qy.group_send_msg("1qaz2wsx3edc123456", "image", {"media_id": "1X0fE0VwakTNduMBQvpZRwedVcQtV_D_4up44ve9dpvXyYIaHGsaxAQcWZ0fT96A8"})
    # qy.group_send_msg("1qaz2wsx3edc123456", "file", {"media_id": txt_media_id})

    # 消息关键字过滤
    # qy.replace_forbid_words(txt_media_id)
