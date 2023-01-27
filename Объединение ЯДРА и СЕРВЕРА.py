import json
import requests
import datetime
from http.server import HTTPServer, CGIHTTPRequestHandler
from threading import *
from time import *

# URL для дадчиков температуры и влажности воздуха
URL_Temperature_AirHumidity = 'https://dt.miet.ru/ppo_it/api/temp_hum/'
# URL для дадчиков влажности почв
URL_GroundHumidity = 'https://dt.miet.ru/ppo_it/api/hum/'
# 'Массив' со всеми данными в формате json
MAS_DATA = {"DATA": []}
print(MAS_DATA['DATA'])
timeout_for_sensors = 5     # таймаут для запросов на сервер теплицы
time_for_reloading = 60     # интервал считывания данных

def data_from_teplica():
    while True:
        # ОТВЕТЫ СЕРВЕРА ПО ТЕМПЕРАТУРЕ И ВЛАЖНОСТИ ВОЗДУХА
        # Массив с данными с датчиков, за последние 5сек
        data_per_5sec = {'timeAIR': 0, 'timeGROUND': 0, 'data': {'air': [], 'ground': []}}
        # Время начала отправки первого запроса в UNIX
        T1_1 = datetime.datetime.now()
        T1_1 = (T1_1 - datetime.datetime(1970, 1, 1)).total_seconds()
        # Создание цикла с обращениями к серверу (температура + влажность воздуха)
        for i in range(1, 5):
            try:
                k = requests.get(URL_Temperature_AirHumidity + str(i), timeout = timeout_for_sensors)
            except Exception:
                data_per_5sec['data']['air'].append({'result': False, 'id': i})
            else:
                data_per_5sec['data']['air'].append({'result': True, 'id': i, 'temperature': k.json()['temperature'], 'humidity': k.json()['humidity']})
            print(data_per_5sec['data']['air'][i - 1])
        # Время получения всех запросов с теплицы (влажность воздуха и его температура) в UNIX
        T1_2 = datetime.datetime.now()
        T1_2 = (T1_2 - datetime.datetime(1970, 1, 1)).total_seconds()
        # ОТВЕТЫ СЕРВЕРА ПО ВЛАЖНОСТИ ПОЧВ
        # Время начала отправки первого запроса в UNIX
        T2_1 = datetime.datetime.now()
        T2_1 = (T2_1 - datetime.datetime(1970, 1, 1)).total_seconds()
        # Создание цикла с обращениями к серверу (влажность почв)
        for i in range(1, 7):
            try:
                k = requests.get(URL_GroundHumidity + str(i), timeout = timeout_for_sensors)
            except Exception:
                data_per_5sec['data']['ground'].append({'result': False, 'id': i})
            else:
                data_per_5sec['data']['ground'].append({'result': True, 'id': i, 'humidity': k.json()['humidity']})
            print(data_per_5sec['data']['ground'][i - 1])
        # Время получения всех запросов с теплицы (влажность почв)
        T2_2 = datetime.datetime.now()
        T2_2 = (T2_2 - datetime.datetime(1970, 1, 1)).total_seconds()
        # Выделения среднего времени для датчиков
        unixT1 = (T1_2 + T1_1) // 2
        ts1 = int(str(unixT1)[:-2])
        value1 = gmtime(ts1)
        T1 = strftime("%Y-%m-%d %H:%M:%S", value1)

        unixT2 = (T2_2 + T2_1) // 2
        ts2 = int(str(unixT2)[:-2])
        value2 = gmtime(ts2)
        T2 = strftime("%Y-%m-%d %H:%M:%S", value2)
        # Добавление времени в кортеж
        data_per_5sec['timeAIR'] = T1
        data_per_5sec['timeGROUND'] = T2

        print(data_per_5sec)
        MAS_DATA["DATA"].append(data_per_5sec)

        sleep(time_for_reloading)
# Запуск функции по считыванию данных с теплицы
data_from_teplica()
