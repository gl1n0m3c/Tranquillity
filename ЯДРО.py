import json
import requests
import time
import datetime

URL_Temperature_AirHumidity_1 = 'https://dt.miet.ru/ppo_it/api/temp_hum/1'
URL_Temperature_AirHumidity_2 = 'https://dt.miet.ru/ppo_it/api/temp_hum/2'
URL_Temperature_AirHumidity_3 = 'https://dt.miet.ru/ppo_it/api/temp_hum/3'
URL_Temperature_AirHumidity_4 = 'https://dt.miet.ru/ppo_it/api/temp_hum/4'
while True:
    print('-----')
    answer_Temperature_AirHumidity_1 = requests.get(URL_Temperature_AirHumidity_1)
    answer_Temperature_AirHumidity_2 = requests.get(URL_Temperature_AirHumidity_2)
    answer_Temperature_AirHumidity_3 = requests.get(URL_Temperature_AirHumidity_3)
    answer_Temperature_AirHumidity_4 = requests.get(URL_Temperature_AirHumidity_4)
    TIME_request = str(datetime.datetime.now())[0:-7]
    # Проверка ответа от датчика 1
    if answer_Temperature_AirHumidity_1.status_code == 200:
        # Создаем переменную в формате json, которую я буду передовать Максу
        data_1 = {
            "id": answer_Temperature_AirHumidity_1.json()["id"],
            "temperature": answer_Temperature_AirHumidity_1.json()["temperature"],
            "humidity": answer_Temperature_AirHumidity_1.json()["humidity"],
            "time": TIME_request
        }
    else:
        print(answer_Temperature_AirHumidity.status_code)
    # Проверка ответа от датчика 2
    if answer_Temperature_AirHumidity_2.status_code == 200:
        # Создаем переменную в формате json, которую я буду передовать Максу
        data_2 = {
            "id": answer_Temperature_AirHumidity_2.json()["id"],
            "temperature": answer_Temperature_AirHumidity_2.json()["temperature"],
            "humidity": answer_Temperature_AirHumidity_2.json()["humidity"],
            "time": TIME_request
        }
    else:
        print(answer_Temperature_AirHumidity.status_code)
    # Проверка ответа от датчика 3
    if answer_Temperature_AirHumidity_3.status_code == 200:
        # Создаем переменную в формате json, которую я буду передовать Максу
        data_3 = {
            "id": answer_Temperature_AirHumidity_3.json()["id"],
            "temperature": answer_Temperature_AirHumidity_3.json()["temperature"],
            "humidity": answer_Temperature_AirHumidity_3.json()["humidity"],
            "time": TIME_request
        }
    else:
        print(answer_Temperature_AirHumidity.status_code)
    # Проверка ответа от датчика 4
    if answer_Temperature_AirHumidity_4.status_code == 200:
        # Создаем переменную в формате json, которую я буду передовать Максу
        data_4 = {
            "id": answer_Temperature_AirHumidity_4.json()["id"],
            "temperature": answer_Temperature_AirHumidity_4.json()["temperature"],
            "humidity": answer_Temperature_AirHumidity_4.json()["humidity"],
            "time": TIME_request
        }
    else:
        print(answer_Temperature_AirHumidity.status_code)
    # Вывод файла в формате JSON
    print(data_1)
    print(data_2)
    print(data_3)
    print(data_4)
    time.sleep(4)