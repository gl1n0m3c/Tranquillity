import requests

URL = 'https://dt.miet.ru/ppo_it/api/total_hum'
response = requests.patch(URL)
print(response.json())