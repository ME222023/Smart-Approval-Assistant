import requests
import json
from typing import List


def get_answer(query: str, conversation_id: str = None) -> str:
    """
    调用"运维智能助手"LLM流程得到回复字符串
    LLM流程：提取"tasks_id"，以JSON格式输出
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

def get_tasks_id_category(query: str, conversation_id: str = None) -> str:
    """
    调用"审批指令分类"LLM流程得到回复字符串
    LLM流程：提取"tasks_id"和"category"，以JSON格式输出
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

    return response.json().get('answer')

def get_names(query: str, conversation_id: str = None) -> List[str]:
    """
    调用"审批指令分类"LLM流程得到回复字符串
    LLM流程：提取"names"后，以字符串列表格式输出
    @param query: 申请者的请求字符串
    @param conversation_id: 申请者的对话ID
    @return: 返回names的字符串列表
    """
    api_key = "app-34mv9GOAdFzrOZLXVJqGV6R0"
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
    reply = response.json().get('answer')
    result = json.loads(reply)
    names = result.get('names')
    
    return names