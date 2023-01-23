import json
import requests

URL = 'https://dt.miet.ru/ppo_it/api/total_hum'
token = {"X-Auth-Token": "97UviE"}

r = requests.patch('https://dt.miet.ru/ppo_it/api/watering', params={"id": 1, "state": 0})
print(r.status_code)
print(r.headers)
print(r.json())