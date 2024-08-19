import requests
import json

# api_key = "app-vdxlirpInaNyVZKhKSk99k3U"
# url = 'http://10.5.5.73:10012/v1/chat-messages'
# headers = {
#     'Authorization': f"Bearer {api_key}",
#     'Content-Type': 'application/json'
# }

# data = {
#     "inputs": {},
#     "query": "What are the specs of the iPhone 13 Pro Max?",
#     # "response_mode": "streaming",
#     "conversation_id": "",
#     "user": "17369c736ab9e12dd4c5fb94e338ff78",
#     "files": [
#         {
#             "type": "image",
#             "transfer_method": "remote_url",
#             "url": "https://cloud.dify.ai/logo/logo-site.png"
#         }
#     ]
# }

# response = requests.post(url, headers=headers, data=json.dumps(data))
# response_json = response.json()
# if 'answer' in response_json:
#         answer = response_json['answer']
# print(response.status_code)
# print(response.json())

def get_answer(query:str,conversation_id:str=None)->str:
    """
    调用"运维智能助手"LLM流程得到回复字符串
    @param query: 申请者的请求字符串
    @param conversation_id: 申请者的对话ID
    @return: LLM回复字符串
    """
    api_key = "app-vdxlirpInaNyVZKhKSk99k3U"
    url = 'http://10.5.5.73:10012/v1/chat-messages'
    headers = {
        'Authorization': f"Bearer {api_key}",
        'Content-Type': 'application/json'
    }

    data = {
        "inputs": {},
        "query": query,
        # "response_mode": "streaming",
        "conversation_id": conversation_id,
        "user": "abc-123",
        "files": [
            {
                "type": "image",
                "transfer_method": "remote_url",
                "url": "https://cloud.dify.ai/logo/logo-site.png"
            }
        ]
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    # print(response.status_code)
    # print(response.json())

    return response.json().get('answer')

def getType(query:str,conversation_id:str=None) -> str:
    """
    调用"审批指令分类"LLM流程得到回复字符串
    {"tasks_id" : {},
    "category" : "{{#1723080153788.category#}}"}
    @param query: 申请者的请求字符串
    @param conversation_id: 申请者的对话ID
    @return: LLM回复的字符串
    """
    api_key = "app-gjvp5FeOkgvkr0WqPzaOUyTW"
    url = 'http://10.5.5.73:10012/v1/chat-messages'
    
    headers = {
        'Authorization': f"Bearer {api_key}",
        'Content-Type': 'application/json'
    }

    data = {
        "inputs": {},
        "query": query,
        # "response_mode": "streaming",
        "conversation_id": conversation_id,
        "user": "abc-123"
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    # print(response)
    # print(response.status_code)
    # print(response.json())

    return response.json().get('answer')

from chat.send_app import qywx

if __name__ == '__main__':
    answer = get_answer("请审批数字集市下11200-11205的任务")
    # answer = get_answer("你好")
    # print(type(json.loads(answer)))
    print(answer)

    qw = qywx()
    qw.send_text(answer, ["17a755177f4ad1f1d99bf8042cfbb74a"])  # 返回内容，用户id
