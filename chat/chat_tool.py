import requests
import os
from typing import Dict
Authorization = os.getenv("AUTHORIZATION")
Authorization = "sk-abJaPLBq6Flzmss2F42b03041b6b475891D5EfCb2a84Ab96"


def chat(data: Dict):
    headers = {
        "Authorization": f"Bearer {Authorization}"
    }

    res = requests.post(url="https://llm-oneapi-dev.axzq.com.cn/v1/chat/completions", headers=headers, json=data)
    # res = requests.post(url="http://llm-oneapi-dev.k8sdev.axzq.com.cn/v1/chat/completions", headers=headers, json=data)
    if res.status_code == 200:
        info = res.json()
        ans = info.get("choices")[0].get("message", {})
        return ans
    else:
        return {"error": None, "code": res.status_code, "msg": res.text}


if __name__ == '__main__':
    data = {
        "model": "gpt-3.5-turbo",
        # "model": "gpt-4",
        "messages": [
            {"role": "user",
             "content": "你好啊"}
        ],
        "stream": False,
        "temperature": 0,
        # "max_length": 2000
    }
    print(chat(data))

