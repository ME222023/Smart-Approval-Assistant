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

def get_answer(query:str,conversation_id:str)->str:
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
        "conversation_id": "0dec15ca-b50c-4a67-9150-95b8adbd31c8",
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

    print(response.status_code)

    print(response.json())

    response_json = response.json()
    return response_json.get('answer')


if __name__ == '__main__':
print(get_answer("What are the specs of the iPhone 13 Pro Max?","0dec15ca-b50c-4a67-9150-95b8adbd31c8"))