import requests
import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer, ThreadingHTTPServer
from threading import *
from time import *
import sqlite3
import json



#                                                                   БАЗА ДАННЫХ
# СОЗДАНИЕ ТАБЛИЦ AIR + GROUND
conn = sqlite3.connect('data.db', check_same_thread=False)
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

cur.execute("""CREATE TABLE IF NOT EXISTS options(
    temperature INTEGER,
    air_hum INTEGER,
    gr_hum INTEGER);
""")
conn.commit()


# ЕСЛИ БД ПУСТА, ТО ЗАПОЛНИТЬ ЕЕ НУЛЯМИ
def start_options():
    cur.execute("SELECT * FROM options")
    axc = cur.fetchall()
    if len(axc) == 0:
        cur.execute("INSERT INTO options VALUES (?,?,?)", (0, 0, 0))
        conn.commit()


start_options()


# ФУНКЦИЯ ОБНОВЛЕНИЯ ПОСЛЕДНЕГО ПАРАМЕТРА СРЕДНЕЙ ТЕМПЕРАТУРЫ
def temp_update(t):
    cur.execute("UPDATE options SET temperature = :t", {"t": t})
    conn.commit()


# ФУНКЦИЯ ОБНОВЛЕНИЯ ПОСЛЕДНЕГО ПАРАМЕТРА СРЕДНЕЙ  ВЛАЖНОСТИ ВОЗДУХА
def air_update(ah):
    cur.execute("UPDATE options SET air_hum = :ah", {"ah": ah})
    conn.commit()


# ФУНКЦИЯ ОБНОВЛЕНИЯ ПОСЛЕДНЕГО ПАРАМЕТРА СРЕДНЕЙ ВЛАЖНОСТИ ЗЕМЛИ
def gr_update(gh):
    cur.execute("UPDATE options SET gr_hum = :gh", {"gh": gh})
    conn.commit()


# ФУНКЦИЯ ОБНУЛЕНИЯ ТАБЛИЦЫ
def null():
    cur.execute("DELETE FROM newair;")
    conn.commit()
    cur.execute("DELETE FROM newground;")
    conn.commit()
    cur.execute("DELETE FROM options;")


# ФУНКЦИЯ ЗАПРОСА ДАННЫХ ЗА ОПРЕДЕЛЕННЫЙ ПЕРИОД
def time_period(n):
    if isinstance(n, str):
        if n == '30min':
            cur.execute(
                "SELECT * from newair WHERE time BETWEEN  DATETIME('now','localtime','-30 minutes') and DATETIME('now','localtime') ORDER BY time,id")
            air = cur.fetchall()
            cur.execute(
                "SELECT * from newground WHERE time BETWEEN  DATETIME('now','localtime','-30 minutes') and DATETIME('now','localtime') ORDER BY time,id")
            ground = cur.fetchall()
            final_result = perevod(air, ground)
        elif n == 'hour':
            cur.execute(
                "SELECT * from newair WHERE time BETWEEN  DATETIME('now','localtime','-1 hour') and DATETIME('now','localtime') ORDER BY time,id")
            air = cur.fetchall()
            cur.execute(
                "SELECT * from newground WHERE time BETWEEN  DATETIME('now','localtime','-1 hour') and DATETIME('now','localtime') ORDER BY time,id")
            ground = cur.fetchall()
            final_result = perevod(air, ground)
        elif n == '12hours':
            cur.execute(
                "SELECT * from newair WHERE time BETWEEN  DATETIME('now','localtime','-12 hours') and DATETIME('now','localtime') ORDER BY time,id")
            air = cur.fetchall()
            cur.execute(
                "SELECT * from newground WHERE time BETWEEN  DATETIME('now','localtime','-12 hours') and DATETIME('now','localtime') ORDER BY time,id")
            ground = cur.fetchall()
            final_result = perevod(air, ground)
        elif n == 'day':
            cur.execute(
                "SELECT * from newair WHERE time BETWEEN  DATETIME('now','localtime','-1 day') and DATETIME('now','localtime') ORDER BY time,id")
            air = cur.fetchall()
            cur.execute(
                "SELECT * from newground WHERE time BETWEEN  DATETIME('now','localtime','-1 day') and DATETIME('now','localtime') ORDER BY time,id")
            ground = cur.fetchall()
            final_result = perevod(air, ground)
        elif n == 'month':
            cur.execute(
                "SELECT * from newair WHERE time BETWEEN  DATETIME('now','localtime','-1 month') and DATETIME('now','localtime') ORDER BY time,id")
            air = cur.fetchall()
            cur.execute(
"SELECT * from newground WHERE time BETWEEN  DATETIME('now','localtime','-1 month') and DATETIME('now','localtime') ORDER BY time,id")
            ground = cur.fetchall()
            final_result = perevod(air, ground)
        else:
            return "Неизвестная дата"
        return final_result
    else:
        return "Неверный формат"


# ФУНКЦИЯ ЗАНЕСЕНИЯ ДАННЫХ В ТАБЛИЦУ
def table_append(var):
    # запись в таблицу air
    for i in range(0, 4):
        if (str(var['data']['air'][i]['result']) == 'True'):
            result = str(var['data']['air'][i]['result'])
            id = var['data']['air'][i]['id']
            temperature = float(var['data']['air'][i]['temperature'])
            humidity = float(var['data']['air'][i]['humidity'])
            time = str(var['timeAIR'])
            aird = (result, id, temperature, humidity, time)
            cur.execute("INSERT INTO newair VALUES(?, ?, ?, ?, ?);", aird)
            conn.commit()
            aird = ()
        else:
            result = str(var['data']['air'][i]['result'])
            id = str(var['data']['air'][i]['id'])
            temperature = 'NULL'
            humidity = 'NULL'
            time = var['timeAIR']
            aird = (result, id, temperature, humidity, time)
            cur.execute("INSERT INTO newair VALUES(?, ?, ?, ?, ?);", aird)
            conn.commit()
            aird = ()

    # запись в таблицу ground
    for i in range(0, 6):
        if (str(var['data']['ground'][i]['result']) == 'True'):
            result = str(var['data']['ground'][i]['result'])
            id = str(var['data']['ground'][i]['id'])
            humidity = str(var['data']['ground'][i]['humidity'])
            time = var['timeGROUND']
            grd = (result, id, humidity, time)
            cur.execute("INSERT INTO newground VALUES(?, ?, ?, ?);", grd)
            conn.commit()
            grd = ()
        else:
            result = str(var['data']['ground'][i]['result'])
            id = str(var['data']['ground'][i]['id'])
            humidity = 'NULL'
            time = var['timeAIR']
            grd = (result, id, humidity, time)
            cur.execute("INSERT INTO newground VALUES(?, ?, ?, ?);", grd)
            conn.commit()
            grd = ()


# ФУНКЦИЯ ПЕРЕВОДА ДАННЫХ ИЗ БД В ФОРМАТ JSON
def perevod(air_mas, ground_mas):
    print(len(air_mas), air_mas[-1][1])
    print(len(ground_mas), ground_mas[-1][1])
    # ПРОВЕРКА НА НЕДОСТАЮЩИЕ ДАННЫЕ С ДАТЧИКОВ, КОТОРЫЕ МОГЛИ НЕДОПИСАТЬСЯ ВСЛЕДСТВИЕ ПРЕКРАЩЕНИЯ ПРОГРАММЫ
    if int(air_mas[-1][1]) != 4 or int(ground_mas[-1][1]) != 6:
        # ВЫЗЫВАЕМ ФУНКЦИЮ
        print("ПРОБЛЕМКА")
        return '{"message": "Проблемка!"}'
    ra = 0
    rg = 0
    result = '{"DATA": ['
    while ra < len(air_mas):
        result += '{"timeAIR": \"' + str(air_mas[ra][4]) + '\", "timeGROUND": \"' + str(
            ground_mas[rg][3]) + '\", "data": {"air": ['

        for r in range(ra, ra + 4):
            result += "{\"result\": \"" + str(air_mas[r][0]) + "\", \"id\": " + str(
                air_mas[r][1]) + ", \"temperature\": " + str(
                air_mas[r][2]) + ", \"humidity\": " + str(air_mas[r][3]) + '}, '

        result = result[:len(result) - 2]
        ra += 4
        result += '],"ground": ['
        for r in range(rg, rg + 6):
            result += "{\"result\": \"" + ground_mas[r][0] + "\", \"id\": " + ground_mas[r][1] + ", \"humidity\": " + \
                      ground_mas[r][2] + '}, '
        result = result[:len(result) - 2]
        rg += 6
        result += "]}},"
    result = result[:len(result) - 1]
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
last_GROUND_humidity = [0, 0, 0, 0, 0, 0]  # массив с последними показаниями с датчиков влажности почв
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
                last_GROUND_humidity[i - 1] = (k.json()['humidity'])
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
        sr_humidity_AIR = sr_humidity_AIR / count
        sr_temp = sr_temp / count
        print(data_per_5sec)
        # Заполнение БД данными за минуту
        table_append(data_per_5sec)
        # Задача интервала
        sleep(time_for_reloading)
        # Возвращение параметров в исходное состояние
        sr_humidity_AIR = sr_temp = count = 0
        last_GROUND_humidity = [0, 0, 0, 0, 0, 0]


#                                                                   СЕРВЕРНАЯ ЧАСТЬ

def SERVER():
    class HttpGetHandler(BaseHTTPRequestHandler):
        """Обработчик с реализованным методом do_GET."""
        def do_GET(self):
            # Основные настройки сервера
            self.send_response(200)
            # self.send_header("Content-type", "text/plain")
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            # Массив, в котором хранятятся данные, переданные пользователем через ссылку
            m = self.path[1:].split('/')
            print(m)
            # ЗАПРОС НА ПЕРЕДАЧУ ПОСЛЕДНИХ НАСТРОЕК ПОЛЬЗОВАТЕЛЯ
            if m[0] == 'give_options':
                cur.execute("SELECT temperature, air_hum, gr_hum from options")
                axc = cur.fetchall()
                self.wfile.write(
                    '{"temperature": '.encode() + str(
                        axc[0][0]).encode() + ', "AIRhumidity": '.encode() + str(
                        axc[0][1]).encode() + ', "GROUNDhumidity": '.encode() + str(
                        axc[0][2]).encode() + '}'.encode())

            # ЗАПРОС НА ПЕРЕДАЧУ ДАННЫХ С ТЕПЛИЦЫ
            elif m[0] == 'give_data':
                self.wfile.write(time_period(m[1]).encode())


            # ПРОВЕРКА НА ВОЗМОЖНОСТЬ ОТКРЫТИЯ ФОРТОЧКИ
            elif m[0] == 'open_windows':
                cur.execute("SELECT temperature, air_hum, gr_hum from options")
                axc = cur.fetchall()
                if axc[0][0] < sr_temp:
                    try:
                        k = requests.patch(url='https://dt.miet.ru/ppo_it/api/fork_drive', params={"state": 1})
                    except Exception:
                        self.wfile.write("{\"message\": \"Сервер теплицы не отвечает!\"}".encode())
                    else:
                        self.wfile.write("{\"message\": \"Форточка открыта!\"}".encode())
                else:
                    self.wfile.write("{\"message\": \"Форточка не может быть открыта в связи со слишком малой температурой в теплице!\"}".encode())

            # ПРОВЕРКА НА ВОЗМОЖНОСТЬ ЗАКРЫТИЯ ФОРТОЧКИ
            elif m[0] == 'close_windows':
                try:
                    k = requests.patch(url='https://dt.miet.ru/ppo_it/api/fork_drive', params={"state": 0})
                except Exception:
                    self.wfile.write("{\"message\": \"Сервер теплицы не отвечает!\"}".encode())
                else:
                    self.wfile.write("{\"message\": \"Форточка закрыта!\"}".encode())

            # ПРОВЕРКА НА ВОЗМОЖНОСТЬ ВКЛЮЧЕНИЯ СИСТЕМЫ УВЛАЖНЕНИЯ ВОЗДУХА В ТЕПЛИЦЕ
            elif m[0] == 'start_humidity_system':
                cur.execute("SELECT temperature, air_hum, gr_hum from options")
                axc = cur.fetchall()
                if axc[0][1] > sr_humidity_AIR:
                    try:
                        k = requests.patch(url='https://dt.miet.ru/ppo_it/api/total_hum', params={"state": 1})
                    except Exception:
                        self.wfile.write("{\"message\": \"Сервер теплицы не отвечает!\"}".encode())
                    else:
                        self.wfile.write("{\"message\": \"Система увлажнения включена!\"}".encode())
                else:
                    self.wfile.write("{\"message\": \"Система увлажнения воздуха не может быть включена в связи с избыточной влажностью в теплице!\"}".encode())

            # ПРОВЕРКА НА ВОЗМОЖНОСТЬ ВКЛЮЧЕНИЯ СИСТЕМЫ УВЛАЖНЕНИЯ ВОЗДУХА В ТЕПЛИЦЕ
            elif m[0] == 'stop_humidity_system':
                try:
                    k = requests.patch(url='https://dt.miet.ru/ppo_it/api/total_hum', params={"state": 0})
                except Exception:
                    self.wfile.write("{\"message\": \"Сервер теплицы не отвечает!\"}".encode())
                else:
                    self.wfile.write("{\"message\": \"Система увлажнения воздуха выключена!\"}".encode())
            # ПРОВЕРКА НА ВОЗМОЖНОСТЬ НАЧАЛА ПОЛИВА КОНКРЕТНОЙ БОРОЗДКИ
            elif m[0] == 'start_wattering':
                cur.execute("SELECT temperature, air_hum, gr_hum from options")
                axc = cur.fetchall()
                if axc[0][2] > last_GROUND_humidity[(int(m[1])) - 1]:
                    try:
                        k = requests.patch(url='https://dt.miet.ru/ppo_it/api/watering',
                                           params={"id": int(m[1]), "state": 1})
                    except Exception:
                        self.wfile.write("{\"message\": \"Сервер теплицы не отвечает!\"}".encode())
                    else:
                        self.wfile.write("{\"message\": \"Система полива бороздки включена!\"}".encode())
                else:
                    self.wfile.write("{\"message\": \"Система полива не может быть включена в связи с избыточной влажностью в бороздке!\"}".encode())

            # ПРОВЕРКА НА ВОЗМОЖНОСТЬ ПРЕКРАЩЕНИЯ ПОЛИВА КОНКРЕТНОЙ БОРОЗДКИ
            elif m[0] == 'stop_wattering':
                try:
                    k = requests.patch(url='https://dt.miet.ru/ppo_it/api/watering',
                                       params={"id": int(m[1]), "state": 0})
                except Exception:
                    self.wfile.write("{\"message\": \"Сервер теплицы не отвечает!\"}".encode())
                else:
                    self.wfile.write("{\"message\": \"Система полива бороздки выключена!\"}".encode())

            # СОХРАНЕНИЕ ПОСЛЕДНЕГО ПАРАМЕТРА СРЕДНЕЙ ТЕМПЕРАТУРЫ ВОЗДУХА
            elif m[0] == 'save_temperature':
                if m[1].isdigit():
                    temp_update(int(m[1]))
                    self.wfile.write("{\"message\": \"Данные успешно сохранены!\"}".encode())
                else:
                    self.wfile.write("{\"message\": \"Неверный формат ввода!\"}".encode())

            # СОХРАНЕНИЕ ПОСЛЕДНЕГО ПАРАМЕТРА СРЕДНЕЙ ВЛАЖНОСТИ ВОЗДУХА
            elif m[0] == 'save_air_humidity':
                if m[1].isdigit():
                    air_update(int(m[1]))
                    self.wfile.write("{\"message\": \"Данные успешно сохранены!\"}".encode())
                else:
                    self.wfile.write("{\"message\": \"Неверный формат ввода!\"}".encode())

            # СОХРАНЕНИЕ ПОСЛЕДНЕГО ПАРАМЕТРА СРЕДНЕЙ ВЛАЖНОСТИ ПОЧВЫ
            elif m[0] == 'save_ground_humidity':
                if m[1].isdigit():
                    gr_update(int(m[1]))
                    self.wfile.write("{\"message\": \"Данные успешно сохранены!\"}".encode())

                else:
                    self.wfile.write("{\"message\": \"Неверный формат ввода!\"}".encode())

            # ИНАЧЕ
            else:
                self.wfile.write("{\"message\": \"Неверная ссылка!\"}".encode())

    server_addres = ('', 8000)
    httpd = ThreadingHTTPServer(server_addres, HttpGetHandler)
    httpd.serve_forever()


# ОБОЗНАЧЕНИЯ ПОТОКОВ
t1 = Thread(target=TEPLICA, args=())
t2 = Thread(target=SERVER, args=())

# ЗАПУСК ПОТОКОВ
t1.start()
t2.start()