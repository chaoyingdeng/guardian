import requests
import json

url = "https://test.pharmaos.com/gw/api/cms-api-svc/api/chat"

payload = {
    "sessionId": 813,
    "content": "哈哈哈"
}
headers = {
    'Host': 'test.pharmaos.com',
    'TM-Header-Token': 'f977442836e34215be5eb2f704a346c5',

}

response = requests.request("POST", url, headers=headers, data=payload)

print(response)
