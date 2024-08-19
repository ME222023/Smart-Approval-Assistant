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

from send_app import qywx

qw = qywx()

qw.send_text("HHHHHHHHHa", ["1730846d950e0a5709ac2ea44138df09"])

if __name__ == '__main__':
    answer = get_answer("请审批数字集市下11200-11205的任务")
    print(type(answer))
    print(answer)