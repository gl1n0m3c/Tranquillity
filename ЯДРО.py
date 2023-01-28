import json
import requests
import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer, ThreadingHTTPServer
from threading import *
from time import *


#                                                                   ЧАСТЬ СО СЧИТЫВАНИЕМ ДАННЫХ С ТЕПЛИЦЫ
# URL для дадчиков температуры и влажности воздуха
URL_Temperature_AirHumidity = 'https://dt.miet.ru/ppo_it/api/temp_hum/'
# URL для дадчиков влажности почв
URL_GroundHumidity = 'https://dt.miet.ru/ppo_it/api/hum/'
# 'Массив' со всеми данными в формате json
MAS_DATA = {"DATA": []}
print(MAS_DATA['DATA'])
timeout_for_sensors = 5  # таймаут для запросов на сервер теплицы
time_for_reloading = 60  # интервал считывания данных
sr_temp = 0  # средняя температура
sr_humidity_AIR = 0  # средняя влажность воздуха
last_GROUND_humidity = [] # массив с последними показаниями с датчиков влажности почв
def TEPLICA():
    while True:
        global sr_temp
        global sr_humidity_AIR
        global last_GROUND_humidity
        count = 0
        # ОТВЕТЫ СЕРВЕРА ПО ТЕМПЕРАТУРЕ И ВЛАЖНОСТИ ВОЗДУХА
        # Массив с данными с датчиков, за последние 5сек
        data_per_5sec = {'timeAIR': 0, 'timeGROUND': 0, 'data': {'air': [], 'ground': []}}
        # Время начала отправки первого запроса в UNIX
        T1_1 = datetime.datetime.now()
        T1_1 = (T1_1 - datetime.datetime(1970, 1, 1)).total_seconds()
        # Создание цикла с обращениями к серверу (температура + влажность воздуха)
        for i in range(1, 5):
            try:
                k = requests.get(URL_Temperature_AirHumidity + str(i), timeout=timeout_for_sensors)
            except Exception:
                data_per_5sec['data']['air'].append({'result': False, 'id': i})
            else:
                count += 1
                sr_temp += k.json()['temperature']
                sr_humidity_AIR += k.json()['humidity']
                data_per_5sec['data']['air'].append(
                    {'result': True, 'id': i, 'temperature': k.json()['temperature'], 'humidity': k.json()['humidity']})
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
                k = requests.get(URL_GroundHumidity + str(i), timeout=timeout_for_sensors)
            except Exception:
                data_per_5sec['data']['ground'].append({'result': False, 'id': i})
                last_GROUND_humidity.append(-1)
            else:
                last_GROUND_humidity.append(k.json()['humidity'])
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
        # Приведение средних параметров в нормальное состояние))
        sr_humidity_AIR = sr_humidity_AIR/count
        sr_temp = sr_temp/count
        print(data_per_5sec)
        MAS_DATA["DATA"].append(data_per_5sec)
        print(sr_humidity_AIR)
        print(sr_temp)
        print(last_GROUND_humidity)
        # Задача интервала
        sleep(time_for_reloading)
        # Возвращение параметров в исходное состояние
        sr_humidity_AIR = sr_temp = count = 0
        last_GROUND_humidity = []



#                                                                   СЕРВЕРНАЯ ЧАСТЬ

def SERVER():
    class HttpGetHandler(BaseHTTPRequestHandler):
        """Обработчик с реализованным методом do_GET."""
        def do_GET(self):
            # Основные настройки сервера
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write('<html><head><meta charset="utf-8">'.encode())
            self.wfile.write('<title>Локальный сервер для передачи данных!</title></head>'.encode())
            # Массив, в котором хранятятся данные, переданные пользователем через ссылку
            m = self.path[1:].split('/')
            print(m)

            # ЗАПРОС НА ПЕРЕДАЧУ ПОСЛЕДНИХ НАСТРОЕК ПОЛЬЗОВАТЕЛЯ
            '''необхоидмо прописать условия, так как пока я не работаю с бд'''
            if m[0] == 'give_options':
                self.wfile.write(
                    '<body>'.encode() + '{"temperature": 30, "AIRhumidity": 60, "GROUNDhumidity": 70}'.encode() + '</body></html>'.encode())

            # ЗАПРОС НА ПЕРЕДАЧУ ДАННЫХ С ТЕПЛИЦЫ
            elif m[0] == 'give_data':
                self.wfile.write(
                    '<body>'.encode() + '{"DATA": [{"timeAIR": "2023-01-23 18:17:39", "timeGROUND": "2023-01-23 18:17:39", "data":{"air": [{"result": "True", "id": 1, "temperature": 27.85, "humidity": 46.92},{"result": "True", "id": 2, "temperature": 29.95, "humidity": 67.55},{"result": "True", "id": 3, "temperature": 29.1, "humidity": 72.91},{"result": "True", "id": 4, "temperature": 29.28, "humidity": 56.81}],"ground": [{"result": "True", "id": 1, "humidity": 72.02},{"result": "True", "id": 2, "humidity": 62.21},{"result": "True", "id": 3, "humidity": 74.5},{"result": "True", "id": 4, "humidity": 72.24},{"result": "True", "id": 5, "humidity": 70.33}, {"result": "True", "id": 6, "humidity": 72.16}]}},{"timeAIR": "2023-01-23 18:17:43", "timeGROUND": "2023-01-23 18:17:44", "data": {"air": [{"result": "True", "id": 1, "temperature": 27.16, "humidity": 47.93}, {"result": "True", "id": 2, "temperature": 29.9, "humidity": 49.35}, {"result": "True", "id": 3, "temperature": 29.31, "humidity": 60.92}, {"result": "True", "id": 4, "temperature": 29.54, "humidity": 81.54}], "ground": [{"result": "True", "id": 1, "humidity": 65.6}, {"result": "True", "id": 2, "humidity": 64.3}, {"result": "True", "id": 3, "humidity": 71.69}, {"result": "True", "id": 4, "humidity": 68.01}, {"result": "True", "id": 5, "humidity": 70.87}, {"result": "True", "id": 6, "humidity": 70.8}]}}, {"timeAIR": "2023-01-23 18:17:48", "timeGROUND": "2023-01-23 18:17:48", "data": {"air": [{"result": "True", "id": 1, "temperature": 27.21, "humidity": 70.57}, {"result": "True", "id": 2, "temperature": 31.63, "humidity": 43.44}, {"result": "True", "id": 3, "temperature": 30.38, "humidity": 56.67}, {"result": "True", "id": 4, "temperature": 29.3, "humidity": 50.43}], "ground": [{"result": "True", "id": 1, "humidity": 62.22}, {"result": "True", "id": 2, "humidity": 73.58}, {"result": "True", "id": 3, "humidity": 64.16}, {"result": "True", "id": 4, "humidity": 73.88}, {"result": "True", "id": 5, "humidity": 68.94}, {"result": "True", "id": 6, "humidity": 72.57}]}}, {"timeAIR": "2023-01-23 18:17:53", "timeGROUND": "2023-01-23 18:17:53", "data": {"air": [{"result": "True", "id": 1, "temperature": 28.28, "humidity": 51.25}, {"result": "True", "id": 2, "temperature": 28.62, "humidity": 80.65}, {"result": "True", "id": 3, "temperature": 28.63, "humidity": 67.72}, {"result": "True", "id": 4, "temperature": 29.8, "humidity": 64.11}], "ground": [{"result": "True", "id": 1, "humidity": 62.54}, {"result": "True", "id": 2, "humidity": 74.42}, {"result": "True", "id": 3, "humidity": 67.02}, {"result": "True", "id": 4, "humidity": 75.1}, {"result": "True", "id": 5, "humidity": 73.04}, {"result": "True", "id": 6, "humidity": 70.7}]}},{"timeAIR": "2023-01-23 18:17:53", "timeGROUND": "2023-01-23 18:17:53", "data": {"air": [{"result": "True", "id": 1, "temperature": 28.28, "humidity": 51.25}, {"result": "True", "id": 2, "temperature": 28.62, "humidity": 80.65}, {"result": "True", "id": 3, "temperature": 28.63, "humidity": 67.72}, {"result": "True", "id": 4, "temperature": 29.8, "humidity": 64.11}], "ground": [{"result": "True", "id": 1, "humidity": 62.54}, {"result": "True", "id": 2, "humidity": 74.42}, {"result": "True", "id": 3, "humidity": 67.02}, {"result": "True", "id": 4, "humidity": 75.1}, {"result": "True", "id": 5, "humidity": 73.04}, {"result": "True", "id": 6, "humidity": 70.7}]}}, {"timeAIR": "2023-01-23 18:17:57", "timeGROUND": "2023-01-23 18:17:57", "data": {"air": [{"result": "True", "id": 1, "temperature": 32.98, "humidity": 42.82}, {"result": "True", "id": 2, "temperature": 30.12, "humidity": 49.43}, {"result": "True", "id": 3, "temperature": 29.38, "humidity": 48.58}, {"result": "True", "id": 4, "temperature": 29.1, "humidity": 82.99}], "ground": [{"result": "True", "id": 1, "humidity": 62.2}, {"result": "True", "id": 2, "humidity": 66.91}, {"result": "True", "id": 3, "humidity": 70.06}, {"result": "True", "id": 4, "humidity": 64.83}, {"result": "True", "id": 5, "humidity": 73.31}, {"result": "True", "id": 6, "humidity": 70.36}]}}, {"timeAIR": "2023-01-23 18:18:02", "timeGROUND": "2023-01-23 18:18:02", "data": {"air": [{"result": "True", "id": 1, "temperature": 30.13, "humidity": 50.93}, {"result": "True", "id": 2, "temperature": 27.7, "humidity": 46.62}, {"result": "True", "id": 3, "temperature": 28.48, "humidity": 62.15}, {"result": "True", "id": 4, "temperature": 29.4, "humidity": 51.31}], "ground": [{"result": "True", "id": 1, "humidity": 77.52}, {"result": "True", "id": 2, "humidity": 76.73}, {"result": "True", "id": 3, "humidity": 68.87}, {"result": "True", "id": 4, "humidity": 65.83}, {"result": "True", "id": 5, "humidity": 74.84}, {"result": "True", "id": 6, "humidity": 70.53}]}}, {"timeAIR": "2023-01-23 18:18:06", "timeGROUND": "2023-01-23 18:18:06", "data": {"air": [{"result": "True", "id": 1, "temperature": 29.21, "humidity": 43.78}, {"result": "True", "id": 2, "temperature": 29.09, "humidity": 80.03}, {"result": "True", "id": 3, "temperature": 28.13, "humidity": 79.29}, {"result": "True", "id": 4, "temperature": 29.85, "humidity": 75.63}], "ground": [{"result": "True", "id": 1, "humidity": 65.68}, {"result": "True", "id": 2, "humidity": 72.53}, {"result": "True", "id": 3, "humidity": 76.46}, {"result": "True", "id": 4, "humidity": 65.98}, {"result": "True", "id": 5, "humidity": 66.78}, {"result": "True", "id": 6, "humidity": 73.31}]}}, {"timeAIR": "2023-01-23 18:18:11", "timeGROUND": "2023-01-23 18:18:11", "data": {"air": [{"result": "False", "id": 1}, {"result": "True", "id": 2, "temperature": 28.56, "humidity": 70.73}, {"result": "True", "id": 3, "temperature": 30.31, "humidity": 45.91}, {"result": "True", "id": 4, "temperature": 29.96, "humidity": 78.8}], "ground": [{"result": "True", "id": 1, "humidity": 62.4}, {"result": "True", "id": 2, "humidity": 77.44}, {"result": "True", "id": 3, "humidity": 71.86}, {"result": "True", "id": 4, "humidity": 71.43}, {"result": "True", "id": 5, "humidity": 69.63}, {"result": "True", "id": 6, "humidity": 69.75}]}}, {"timeAIR": "2023-01-23 18:18:15", "timeGROUND": "2023-01-23 18:18:15", "data": {"air": [{"result": "True", "id": 1, "temperature": 31.64, "humidity": 63.1}, {"result": "True", "id": 2, "temperature": 30.6, "humidity": 64.13}, {"result": "True", "id": 3, "temperature": 30.44, "humidity": 77.35}, {"result": "False", "id": 4}], "ground": [{"result": "True", "id": 1, "humidity": 67.29}, {"result": "True", "id": 2, "humidity": 69.78}, {"result": "True", "id": 3, "humidity": 69.06}, {"result": "True", "id": 4, "humidity": 64.29}, {"result": "True", "id": 5, "humidity": 73.23}]}}]}'.encode() + '</body></html>'.encode())

            # ПРОВЕРКА НА ВОЗМОЖНОСТЬ ОТКРЫТИЯ ФОРТОЧКИ
            elif m[0] == 'open_windows':
                try:
                    k = requests.patch(url = 'https://dt.miet.ru/ppo_it/api/fork_drive/', params = {"state": 1})
                except Exception:
                    self.wfile.write('<body>'.encode() + '{"message": "Сервер теплицы не отвечает!"}'.encode() + '</body></html>'.encode())
                else:
                    self.wfile.write(
                        '<body>'.encode() + '{"message": "Форточка открыта!"}'.encode() + '</body></html>'.encode())
                self.wfile.write(
                    '<body>'.encode() + '{"message": "Форточка не может быть открыта в связи со слишком малой температурой в теплице!"}'.encode() + '</body></html>'.encode())

            # ПРОВЕРКА НА ВОЗМОЖНОСТЬ ЗАКРЫТИЯ ФОРТОЧКИ
            elif m[0] == 'close_windows':
                try:
                    k = requests.patch(url='https://dt.miet.ru/ppo_it/api/fork_drive', params={"state": 0})
                except Exception:
                    self.wfile.write(
                        '<body>'.encode() + '{"message": "Сервер теплицы не отвечает!"}'.encode() + '</body></html>'.encode())
                else:
                    self.wfile.write(
                        '<body>'.encode() + '{"message": "Форточка закрыта!"}'.encode() + '</body></html>'.encode())
                    print(sr_temp, last_GROUND_humidity, sr_humidity_AIR)

            # ПРОВЕРКА НА ВОЗМОЖНОСТЬ ВКЛЮЧЕНИЯ СИСТЕМЫ УВЛАЖНЕНИЯ В ТЕПЛИЦЕ
            elif m[0] == 'start_humidity_system':
                # Отправка серверу теплицы запрос на включение системы увлажнения
                '''Дописать проверку условия с параметрами из БД'''
                try:
                    k = requests.patch(url = 'https://dt.miet.ru/ppo_it/api/total_hum', params = {"state": 1})
                except Exception:
                    self.wfile.write('<body>'.encode() + '{"message": "Сервер теплицы не отвечает!"}'.encode() + '</body></html>'.encode())
                else:
                    self.wfile.write(
                        '<body>'.encode() + '{"message": "Система увлажнения включена!"}'.encode() + '</body></html>'.encode())
                self.wfile.write(
                    '<body>'.encode() + '{"message": "Система увлажнения воздуха не может быть включена в связи с избыточной влажностью в теплице!"}'.encode() + '</body></html>'.encode())

            # ПРОВЕРКА НА ВОЗМОЖНОСТЬ ВКЛЮЧЕНИЯ СИСТЕМЫ УВЛАЖНЕНИЯ В ТЕПЛИЦЕ
            elif m[0] == 'off_humidity_system':
                try:
                    k = requests.patch(url = 'https://dt.miet.ru/ppo_it/api/total_hum', params = {"state": 0})
                except Exception:
                    self.wfile.write(
                        '<body>'.encode() + '{"message": "Сервер теплицы не отвечает!"}'.encode() + '</body></html>'.encode())
                else:
                    self.wfile.write(
                        '<body>'.encode() + '{"message": "Система увлажнения воздуха выключена!"}'.encode() + '</body></html>'.encode())

            # ПРОВЕРКА НА ВОЗМОЖНОСТЬ ПОЛИВА КОНКРЕТНОЙ БОРОЗДКИ
            elif m[0] == 'start_wattering':
                self.wfile.write(
                    '<body>'.encode() + '{"message": "Система полива включена!"}'.encode() + '</body></html>'.encode())
                self.wfile.write(
                    '<body>'.encode() + '{"message": "Система полива не может быть включена в связи с избыточной влажностью в бороздке!"}'.encode() + '</body></html>'.encode())
            else:
                self.wfile.write(
                    '<body>'.encode() + '{"message": "Неверная ссылка!"}'.encode() + '</body></html>'.encode())

    server_addres = ('', 8000)
    httpd = ThreadingHTTPServer(server_addres, HttpGetHandler)
    httpd.serve_forever()

# ОБОЗНАЧЕНИЯ ПОТОКОВ
t1 = Thread(target = TEPLICA, args = ())
t2 = Thread(target = SERVER, args = ())

# ЗАПУСК ПОТОКОВ
t1.start()
t2.start()
