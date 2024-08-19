import requests
from urllib.parse import unquote, quote

def check_totoal_api():
    data = ""

    # 配置
    sToken = "hJqcu3uJ9Tn2gXPmxx2w9kkCkCE2EPYo"
    sEncodingAESKey = "6qkdMrq68nTKduznJYO1A37W2oEgpkMUvkttRToqhUt"
    sCorpID = "ww1436e0e65a779aee"


    # 验证回调URL
    # echstr = "fsi1xnbH4yQh0+PJxcOdhhK6TDXkjMyhEPA7xB2TGz6b+g7xyAbEkRxN/3cNXW9qdqjnoVzEtpbhnFyq6SVHyA=="
    # url = f"http://10.5.5.73:10051/weichat?msg_signature=e4ce8c72f1ba7b000cafd9b3be071938215a7f29&timestamp=1707119034&nonce=1707096696&echostr=aE2cFYygMV78gBACE8At1GaW8XNQozEzXo3w6pHuBe%2FUTVZ%2FAm0aBvCPbXimAHTHsxLCIZyCJU6GPeltcHDmxg%3D%3D"
    # res = requests.get(url)

    # 对用户回复的消息解密
    ## 文本
    # headers = {'Content-Type': 'application/xml'}
    # sReqData = "<xml><ToUserName><![CDATA[ww8da50fdd614a1fb6]]></ToUserName><Encrypt><![CDATA[ofcS08cTD3qcsDmIzizciAFZAZbL4xdjmfVPafQ+5HM3LWluReIynboN9ZYLA34OdRbNGIbjnSbvSa+Mky3pYzwlptcZdCims5oQ3L/ms7J8oHfL1LefgL88xa4NGZzTMQx93vAQvZWBSNk9h/gaHqTBtuDLxX2VvbeWe9HDmfqN5horRyeyW5qPXXUHLsfmzR/1a3jclO02/yo7Am4AMLbtr8pcKSLFx0dYjXEJeOFssrDuMeAPfaQT9rAhum5yK3IpvXOaU/dssTqE7bYHXtIB0bSYzc9NqTMMSU8TmjTx84k3VDlFwPaldBF8oW6SC5STwMJBo4N1ITDMOUlUskSFXDlI5iJAJ4qwmKHvXTJx9bLWZSSJ+b89zjEaU/S4ulWlj1ID5wC7m6QWCkLbaEdIv5xGSvo1qZ/t5uWY78dPRuCY9TQxj+a1vRyL0hA/9al+MyoommXcb6xwzJ3OzA==]]></Encrypt><AgentID><![CDATA[1000188]]></AgentID></xml>"
    # url = f"http://10.5.5.73:10051/weichat?msg_signature=4569d01182484f6f5353de46b15eb6cd24c5aba0&timestamp=1707183465&nonce=1707980560"
    # res = requests.post(url, data=sReqData.encode("utf-8"), headers=headers)

    ## 图片
    # headers = {'Content-Type': 'application/xml'}
    sReqData = """<xml>
    <ToUserName><![CDATA[ww8da50fdd614a1fb6]]></ToUserName>
    <Encrypt><![CDATA[oSK4q1LCYx3eyNHO1Zdpgq0cbzGZsom2+X2TH7ER+1EqQFoqPEedNJOwjwXrAlytejs4qKXxdKNKVn1PKjKv6cixm4UaxUBL7m4AACrTkrtdPWQnvDQI+mpKv80aenCRfwQp3OY56HDoQtOzCHzdoQzJAyWy3l7uXpgtd56gGynqDf0S1EfcnpTJ6wW0V22wV+SjTgPDMJ8GsrKRwZ12n3OnlAcVCwPcb3L7/Q+4upwhQ+PhyKhiRtpP4qk3KTI+KsOsYGgxCiNbx3lljP4h0l6hlDOvbdzTWcn0cE9vqRf892AERwkccWdMa9PYjR6hnEmVQopTU9ZRFJuOk6YW1Lgpkl/ZWUu84QvDd+cWbQb9u3rbQ3HrYAQ7wl8rCPiKKeq9J4SIhJ4f/YxR5xV/WPFft1dIT/Hebn91VJTmbJB+fhilvgNPaQkuf5MhdDAcsmZZ7Ukrd1qoSRWuXkR8xczk5LZUW0mpRmZflSDOysQ5lQ4C/PTZ90dqqU5tM0WQCKgRCze7ZDv4GV71tOwD47WJAw1KYvyJvaaIFYba+Yk=]]></Encrypt>
    <AgentID><![CDATA[1000188]]></AgentID>
    </xml>"""
    url = "http://10.5.5.73:10051/weichat?msg_signature=d0eacda4fea0486ad93ce27849f5c4da2164a9d6&timestamp=1707204221&nonce=1707952350"
    res = requests.post(url, data=sReqData.encode("utf-8"))
    print(res.text)


if __name__ == "__main__":
    pass
    check_totoal_api()
