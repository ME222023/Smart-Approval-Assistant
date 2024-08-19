url = 'http://10.5.5.73/v1/workflows/run'

header = {
    "Authorization": 
}
--header 'Authorization: Bearer {api_key}' \
--header 'Content-Type: application/json' \
--data-raw '{
    "inputs": {你好，可以帮我审批调度吗？},
    "response_mode": "streaming",
    "user": "abc-123"
}'