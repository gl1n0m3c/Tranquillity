import json
import requests
import time
import datetime


URL_Temperature_AirHumidity_1 = 'https://dt.miet.ru/ppo_it/api/temp_hum/1'
URL_Temperature_AirHumidity_2 = 'https://dt.miet.ru/ppo_it/api/temp_hum/2'
URL_Temperature_AirHumidity_3 = 'https://dt.miet.ru/ppo_it/api/temp_hum/3'
URL_Temperature_AirHumidity_4 = 'https://dt.miet.ru/ppo_it/api/temp_hum/4'
MAS_DATA = {"DATA": []}
print(MAS_DATA['DATA'])
while True:
    print('-----')
    answer_Temperature_AirHumidity_1 = requests.get(URL_Temperature_AirHumidity_1)
    answer_Temperature_AirHumidity_2 = requests.get(URL_Temperature_AirHumidity_2)
    TIME_request = str(datetime.datetime.now())[0:-7]
    answer_Temperature_AirHumidity_3 = requests.get(URL_Temperature_AirHumidity_3)
    answer_Temperature_AirHumidity_4 = requests.get(URL_Temperature_AirHumidity_4)
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