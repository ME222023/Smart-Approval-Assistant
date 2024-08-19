import requests
url = 'http://10.5.5.73/v1/workflows/run'

api_key = "app-w9C19WBHnmBHDytEuA8Xakyr"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}
data = {
    "inputs": {"你好，可以帮我审批调度吗？"},
    "response_mode": "streaming",
    "user": "abc-123"
}
res = requests.post(url=url, json=data, headers=headers)