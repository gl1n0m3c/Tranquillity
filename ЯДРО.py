import json
import requests
import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer, ThreadingHTTPServer
from threading import *
from time import *
import sqlite3




#                                                                   БАЗА ДАННЫХ
# СОЗДАНИЕ ТАБЛИЦ AIR + GROUND
conn = sqlite3.connect('data.db', check_same_thread = False)
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS newair(
   result TEXT,
   id INTEGER,
   temperature REAL,
   humidity REAL,
   time TEXT);
""")
conn.commit()
cur.execute("""CREATE TABLE IF NOT EXISTS newground(
   result TEXT,
   id TEXT,  
   humidity TEXT,
   time TEXT);
""")
conn.commit()

# ФУНКЦИЯ ОБНУЛЕНИЯ ТАБЛИЦЫ
def null():
    cur.execute("DELETE FROM newair;")
    conn.commit()
    cur.execute("DELETE FROM newground;")
    conn.commit()

# ФУНКЦИЯ ЗАПРОСА ДАННЫХ ЗА ОПРЕДЕЛЕННЫЙ ПЕРИОД
def time_period(n):
    if isinstance(n, str):
        if n == '30min':
            cur.execute("SELECT * from newair WHERE time BETWEEN  DATETIME('now','localtime','-30 minutes') and DATETIME('now','localtime') ORDER BY time,id")
            air = cur.fetchall()
            cur.execute("SELECT * from newground WHERE time BETWEEN  DATETIME('now','localtime','-30 minutes') and DATETIME('now','localtime') ORDER BY time,id")
            ground = cur.fetchall()
            final_result = perevod(air, ground)
        elif n == 'hour':
            cur.execute("SELECT * from newair WHERE time BETWEEN  DATETIME('now','localtime','-1 hour') and DATETIME('now','localtime') ORDER BY time,id")
            air = cur.fetchall()
            cur.execute("SELECT * from newground WHERE time BETWEEN  DATETIME('now','localtime','-1 hour') and DATETIME('now','localtime') ORDER BY time,id")
            ground = cur.fetchall()
            final_result = perevod(air, ground)
        elif n == '12hours':
            cur.execute("SELECT * from newair WHERE time BETWEEN  DATETIME('now','localtime','-12 hours') and DATETIME('now','localtime') ORDER BY time,id")
            air = cur.fetchall()
            cur.execute("SELECT * from newground WHERE time BETWEEN  DATETIME('now','localtime','-12 hours') and DATETIME('now','localtime') ORDER BY time,id")
            ground = cur.fetchall()
            final_result = perevod(air, ground)
        elif n == 'day':
            cur.execute("SELECT * from newair WHERE time BETWEEN  DATETIME('now','localtime','-1 day') and DATETIME('now','localtime') ORDER BY time,id")
            air = cur.fetchall()
            cur.execute("SELECT * from newground WHERE time BETWEEN  DATETIME('now','localtime','-1 day') and DATETIME('now','localtime') ORDER BY time,id")
            ground = cur.fetchall()
            final_result = perevod(air, ground)
        elif n == 'month':
            cur.execute("SELECT * from newair WHERE time BETWEEN  DATETIME('now','localtime','-1 month') and DATETIME('now','localtime') ORDER BY time,id")
            air = cur.fetchall()
            cur.execute("SELECT * from newground WHERE time BETWEEN  DATETIME('now','localtime','-1 month') and DATETIME('now','localtime') ORDER BY time,id")
            ground = cur.fetchall()
            final_result = perevod(air,ground)
        else:
            return "Неизвестная дата"
        return final_result
    else:
        return "Неверный формат"

# ФУНКЦИЯ ЗАНЕСЕНИЯ ДАННЫХ В ТАБЛИЦУ
def table_append(var):
    # запись в таблицу air
    for i in range(0,4):
        if (str(var['data']['air'][i]['result']) == 'True'):
            result = str(var['data']['air'][i]['result'])
            id = var['data']['air'][i]['id']
            temperature = float(var['data']['air'][i]['temperature'])
            humidity = float(var['data']['air'][i]['humidity'])
            time = str(var['timeAIR'])
            aird = (result,id,temperature,humidity,time)
            cur.execute("INSERT INTO newair VALUES(?, ?, ?, ?, ?);", aird)
            conn.commit()
            aird = ()
        else:
            result = str(var['data']['air'][i]['result'])
            id = str(var['data']['air'][i]['id'])
            temperature = 'NULL'
            humidity = 'NULL'
            time = var['timeAIR']
            aird = (result,id,temperature,humidity,time)
            cur.execute("INSERT INTO newair VALUES(?, ?, ?, ?, ?);", aird)
            conn.commit()
            aird = ()

    # запись в таблицу ground
    for i in range(0,6):
        if (str(var['data']['ground'][i]['result']) == 'True'):
            result = str(var['data']['ground'][i]['result'])
            id = str(var['data']['ground'][i]['id'])
            humidity = str(var['data']['ground'][i]['humidity'])
            time = var['timeGROUND']
            grd = (result,id,humidity,time)
            cur.execute("INSERT INTO newground VALUES(?, ?, ?, ?);", grd)
            conn.commit()
            grd = ()
        else:
            result = str(var['data']['ground'][i]['result'])
            id = str(var['data']['ground'][i]['id'])
            humidity = 'NULL'
            time = var['timeAIR']
            grd = (result,id,humidity,time)
            cur.execute("INSERT INTO newground VALUES(?, ?, ?, ?);", grd)
            conn.commit()
            grd = ()

# ФУНКЦИЯ ПЕРЕВОДА ДАННЫХ ИЗ БД В ФОРМАТ JSON
def perevod(air_mas, ground_mas):
    ra = 0
    rg = 0
    result = '{"DATA": [\n'
    while ra < len(air_mas):
        result += "{'timeAIR':" + str(air_mas[ra][4]) + ",'timeGROUND':" + str(ground_mas[rg][3]) + ",'data':{\n'air': ["
        for r in range(ra,ra+4):
            result += "{'result': " + str(air_mas[r][0]) + ",'id': "       + str(air_mas[r][1]) + ",'temperature': " + \
                                        str(air_mas[r][2]) + ",'humidity': " + str(air_mas[r][3]) + "},\n"
        ra += 4
        result += "],\n'ground': [\n"
        for r in range(rg,rg+6):
            result += "{'result': " + ground_mas[r][0] + ",'id': " + ground_mas[r][1] + ",'humidity': " + ground_mas[r][2] + "},\n"
        rg += 6
        result += "]}},\n"
    result += "]}"
    return result



#                                                                   ЧАСТЬ СО СЧИТЫВАНИЕМ ДАННЫХ С ТЕПЛИЦЫ
# URL для дадчиков температуры и влажности воздуха
URL_Temperature_AirHumidity = 'https://dt.miet.ru/ppo_it/api/temp_hum/'
# URL для дадчиков влажности почв
URL_GroundHumidity = 'https://dt.miet.ru/ppo_it/api/hum/'
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
        # Заполнение БД данными за минуту
        table_append(data_per_5sec)
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
                self.wfile.write('<body>'.encode() + time_period(m[1]).encode() + '</body></html>'.encode())


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
            elif m[0] == 'stop_humidity_system':
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
