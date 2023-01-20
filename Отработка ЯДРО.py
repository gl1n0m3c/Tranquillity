import requests

URL = 'https://dt.miet.ru/ppo_it/api/fork_drive/'
response = requests.patch(URL)
print(response.json())