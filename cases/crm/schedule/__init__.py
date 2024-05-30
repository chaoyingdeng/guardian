import requests

payload = {'page': '1', 'size': '20'}
r = requests.request('get','https://api.github.com/events', params=payload)

print(r.url)