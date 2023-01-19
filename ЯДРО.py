import json
import requests
import time

while True:
    URL_Temperature_AirHumidity = 'https://dt.miet.ru/ppo_it/api/temp_hum/1'
    answer_Temperature_AirHumidity = requests.get(URL_Temperature_AirHumidity)
    if answer_Temperature_AirHumidity.status_code == 200:
        print(answer_Temperature_AirHumidity.json())
        print(answer_Temperature_AirHumidity.status_code)
        print(answer_Temperature_AirHumidity.headers['Date'])
        print('-----')
    else:
        print(answer_Temperature_AirHumidity.status_code)
        # должно передавать статус в БД и передавать это в пользовательский интерфейс
    time.sleep(5)