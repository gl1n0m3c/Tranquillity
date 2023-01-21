import json
import requests
import time
import datetime


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
    # ОТВЕТЫ СЕРВЕРА ПО ТЕМПЕРАТУРЕ И ВЛАЖНОСТИ ВОЗДУХА
    # 1 датчик влажности воздуха и его температуры
    try:
        answer_Temperature_AirHumidity_1 = requests.get(URL_Temperature_AirHumidity_1, timeout = timeout_for_sensors)
    except Exception:
        answer_Temperature_AirHumidity_1 = {'request': False}
    else:
        answer_Temperature_AirHumidity_1 = {
            'request': True,
            'id': 1,
            'temperature': answer_Temperature_AirHumidity_1.json()['temperature'],
            'humidity': answer_Temperature_AirHumidity_1.json()['humidity']
        }
    # 2 датчик влажности воздуха и его температуры
    try:
        answer_Temperature_AirHumidity_2 = requests.get(URL_Temperature_AirHumidity_1, timeout = timeout_for_sensors)
    except Exception:
        answer_Temperature_AirHumidity_2 = {'request': False}
    else:
        answer_Temperature_AirHumidity_2 = {
            'request': True,
            'id': 1,
            'temperature': answer_Temperature_AirHumidity_2.json()['temperature'],
            'humidity': answer_Temperature_AirHumidity_2.json()['humidity']
        }
    # 3 датчик влажности воздуха и его температуры
    try:
        answer_Temperature_AirHumidity_3 = requests.get(URL_Temperature_AirHumidity_1, timeout = timeout_for_sensors)
    except Exception:
        answer_Temperature_AirHumidity_3 = {'request': False}
    else:
        answer_Temperature_AirHumidity_3 = {
            'request': True,
            'id': 1,
            'temperature': answer_Temperature_AirHumidity_3.json()['temperature'],
            'humidity': answer_Temperature_AirHumidity_3.json()['humidity']
        }
    # 4 датчик влажности воздуха и его температуры
    try:
        answer_Temperature_AirHumidity_4 = requests.get(URL_Temperature_AirHumidity_1, timeout = timeout_for_sensors)
    except Exception:
        answer_Temperature_AirHumidity_4 = {'request': False}
    else:
        answer_Temperature_AirHumidity_4 = {
            'request': True,
            'id': 1,
            'temperature': answer_Temperature_AirHumidity_4.json()['temperature'],
            'humidity': answer_Temperature_AirHumidity_4.json()['humidity']
        }
    # Время получения всех запросов с теплицы (влажность воздуха и его температура)
    T1 = str(datetime.datetime.now())[0:-7]
    # ОТВЕТЫ СЕРВЕРА ПО ВЛАЖНОСТИ ПОЧВ
    # 1 датчик влажности почвы
    try:
        answer_GroundHumidity_1 = requests.get(URL_GroundHumidity_1, timeout=timeout_for_sensors)
    except Exception:
        answer_GroundHumidity_1 = {'request': False}
    else:
        answer_GroundHumidity_1 = {
            'request': True,
            'id': 1,
            'humidity': answer_GroundHumidity_1.json()['humidity']
        }
    # 2 датчик влажности почвы
    try:
        answer_GroundHumidity_2 = requests.get(URL_GroundHumidity_2, timeout=timeout_for_sensors)
    except Exception:
        answer_GroundHumidity_2 = {'request': False}
    else:
        answer_GroundHumidity_2 = {
            'request': True,
            'id': 1,
            'humidity': answer_GroundHumidity_2.json()['humidity']
        }
    # 3 датчик влажности почвы
    try:
        answer_GroundHumidity_3 = requests.get(URL_GroundHumidity_3, timeout=timeout_for_sensors)
    except Exception:
        answer_GroundHumidity_3 = {'request': False}
    else:
        answer_GroundHumidity_3 = {
            'request': True,
            'id': 1,
            'humidity': answer_GroundHumidity_3.json()['humidity']
        }
    # 4 датчик влажности почвы
    try:
        answer_GroundHumidity_4 = requests.get(URL_GroundHumidity_4, timeout=timeout_for_sensors)
    except Exception:
        answer_GroundHumidity_4 = {'request': False}
    else:
        answer_GroundHumidity_4 = {
            'request': True,
            'id': 1,
            'humidity': answer_GroundHumidity_4.json()['humidity']
        }
    # 5 датчик влажности почвы
    try:
        answer_GroundHumidity_5 = requests.get(URL_GroundHumidity_5, timeout=timeout_for_sensors)
    except Exception:
        answer_GroundHumidity_5 = {'request': False}
    else:
        answer_GroundHumidity_5 = {
            'request': True,
            'id': 1,
            'humidity': answer_GroundHumidity_5.json()['humidity']
        }
    # 6 датчик влажности почвы
    try:
        answer_GroundHumidity_6 = requests.get(URL_GroundHumidity_6, timeout=timeout_for_sensors)
    except Exception:
        answer_GroundHumidity_6 = {'request': False}
    else:
        answer_GroundHumidity_6 = {
            'request': True,
            'id': 1,
            'humidity': answer_GroundHumidity_6.json()['humidity']
        }
    # Время получения всех запросов с теплицы (влажность почв)
    T2 = str(datetime.datetime.now())[0:-7]
    # Массив с данными с датчиков, за последние 5сек
    data_per_5sec = {'timeAIR': T1,'timeGROUND': T2, 'data':{'air': [], 'ground': []}}
    print("AIR")
    print(answer_Temperature_AirHumidity_1)
    print(answer_Temperature_AirHumidity_2)
    print(answer_Temperature_AirHumidity_3)
    print(answer_Temperature_AirHumidity_4)
    print(T1)
    data_per_5sec['data']['air'].append(answer_Temperature_AirHumidity_1)
    data_per_5sec['data']['air'].append(answer_Temperature_AirHumidity_2)
    data_per_5sec['data']['air'].append(answer_Temperature_AirHumidity_3)
    data_per_5sec['data']['air'].append(answer_Temperature_AirHumidity_4)

    print("GROUND")
    print(answer_GroundHumidity_1)
    print(answer_GroundHumidity_2)
    print(answer_GroundHumidity_3)
    print(answer_GroundHumidity_4)
    print(answer_GroundHumidity_5)
    print(answer_GroundHumidity_6)
    data_per_5sec['data']['ground'].append(answer_GroundHumidity_1)
    data_per_5sec['data']['ground'].append(answer_GroundHumidity_2)
    data_per_5sec['data']['ground'].append(answer_GroundHumidity_3)
    data_per_5sec['data']['ground'].append(answer_GroundHumidity_4)
    data_per_5sec['data']['ground'].append(answer_GroundHumidity_5)
    data_per_5sec['data']['ground'].append(answer_GroundHumidity_6)
    print(T2)

    print(data_per_5sec)
    time.sleep(4)