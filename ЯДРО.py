import json
import requests
import time
from datetime import timezone

# URL для дадчиков температуры и влажности воздуха
URL_Temperature_AirHumidity_1 = 'https://dt.miet.ru/ppo_it/api/temp_hum/1'
URL_Temperature_AirHumidity_2 = 'https://dt.miet.ru/ppo_it/api/temp_hum/2'
URL_Temperature_AirHumidity_3 = 'https://dt.miet.ru/ppo_it/api/temp_hum/3'
URL_Temperature_AirHumidity_4 = 'https://dt.miet.ru/ppo_it/api/temp_hum/4'
# URL для дадчиков влажности почв
URL_GroundHumidity_1 = 'https://dt.miet.ru/ppo_it/api/hum/1'
URL_GroundHumidity_2 = 'https://dt.miet.ru/ppo_it/api/hum/2'
URL_GroundHumidity_3 = 'https://dt.miet.ru/ppo_it/api/hum/3'
URL_GroundHumidity_4 = 'https://dt.miet.ru/ppo_it/api/hum/4'
URL_GroundHumidity_5 = 'https://dt.miet.ru/ppo_it/api/hum/5'
URL_GroundHumidity_6 = 'https://dt.miet.ru/ppo_it/api/hum/6'
# 'Массив' со всеми данными в формате json
MAS_DATA = {"DATA": []}
print(MAS_DATA['DATA'])
timeout_for_sensors = 0.25
while True:
    print('-----')
    # Ответы сервера по температуре и влажности
    answer_Temperature_AirHumidity_1 = requests.get(URL_Temperature_AirHumidity_1, timeout = timeout_for_sensors)
    answer_Temperature_AirHumidity_2 = requests.get(URL_Temperature_AirHumidity_2, timeout = timeout_for_sensors)
    answer_Temperature_AirHumidity_3 = requests.get(URL_Temperature_AirHumidity_3, timeout = timeout_for_sensors)
    answer_Temperature_AirHumidity_4 = requests.get(URL_Temperature_AirHumidity_4, timeout = timeout_for_sensors)
    TIME_request = answer_Temperature_AirHumidity_4.headers['Date']
    print(TIME_request)
    # answer_GroundHumidity_1 = requests.get()
    # Переменная, которая будет хранить данные за последние 5сек
    DATA_per_5sec = {"time": TIME_request, 'data':[]}
    # Проверка ответа от датчика 1
    if answer_Temperature_AirHumidity_1.status_code == 200:
        # Создаем переменную в формате json, которую я буду передовать Максу
        DATA_per_5sec["data"].append({
            "result": True,
            "id": answer_Temperature_AirHumidity_1.json()["id"],
            "temperature": answer_Temperature_AirHumidity_1.json()["temperature"],
            "humidity": answer_Temperature_AirHumidity_1.json()["humidity"],
        })
    else:
        DATA_per_5sec.append({
            "result": False
        })
    # Проверка ответа от датчика 2
    if answer_Temperature_AirHumidity_2.status_code == 200:
        # Создаем переменную в формате json, которую я буду передовать Максу
        DATA_per_5sec["data"].append({
            "result": True,
            "id": answer_Temperature_AirHumidity_2.json()["id"],
            "temperature": answer_Temperature_AirHumidity_2.json()["temperature"],
            "humidity": answer_Temperature_AirHumidity_2.json()["humidity"],
        })
    else:
        DATA_per_5sec.append({
            "result": False
        })
    # Проверка ответа от датчика 3
    if answer_Temperature_AirHumidity_3.status_code == 200:
        # Создаем переменную в формате json, которую я буду передовать Максу
        DATA_per_5sec["data"].append({
            "result": True,
            "id": answer_Temperature_AirHumidity_3.json()["id"],
            "temperature": answer_Temperature_AirHumidity_3.json()["temperature"],
            "humidity": answer_Temperature_AirHumidity_3.json()["humidity"],
        })
    else:
        DATA_per_5sec.append({
            "result": False
        })
    # Проверка ответа от датчика 4
    if answer_Temperature_AirHumidity_4.status_code == 200:
        # Создаем переменную в формате json, которую я буду передовать Максу
        DATA_per_5sec["data"].append({
            "result": True,
            "id": answer_Temperature_AirHumidity_4.json()["id"],
            "temperature": answer_Temperature_AirHumidity_4.json()["temperature"],
            "humidity": answer_Temperature_AirHumidity_4.json()["humidity"],
        })
    else:
        DATA_per_5sec.append({
            "result": False
        })
    # Добавлени в основной массив с данными, данные за 5сек
    MAS_DATA['DATA'].append(DATA_per_5sec)
    print(DATA_per_5sec)
    print(MAS_DATA)
    time.sleep(4)