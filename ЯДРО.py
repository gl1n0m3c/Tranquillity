import requests
import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import *
from time import *
import sqlite3
import datetime as DT



#                                                                   БАЗА ДАННЫХ
# СОЗДАНИЕ ТАБЛИЦ AIR + GROUND
conn = sqlite3.connect('data.db', check_same_thread=False)
cur = conn.cursor()
# создание таблиц air, ground, last_parametr
cur.execute("""CREATE TABLE IF NOT EXISTS air(
   result TEXT,
   id INTEGER,
   temperature REAL,
   humidity REAL,
   time TEXT);
""")
conn.commit()
cur.execute("""CREATE TABLE IF NOT EXISTS ground(
   result TEXT,
   id INTEGER,  
   humidity REAL,
   time TEXT);
""")
conn.commit()
cur.execute("""CREATE TABLE IF NOT EXISTS options(
    temperature INTEGER,
    air_hum INTEGER,
    gr_hum INTEGER);
""")
conn.commit()

# ФУНКЦИЯ ОБНУЛЕНИЯ ВСЕЙ БД
def null():
    cur.execute("DELETE FROM air;")
    conn.commit()
    cur.execute("DELETE FROM ground;")
    conn.commit()
    cur.execute("DELETE FROM options;")


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


# ФУНКЦИЯ УДАЛЕНИЯ ПОСЛЕДНИХ ДАННЫХ, ИСПОЛЬЗУЕМАЯ В СЛУЧАЕ, ЕСЛИ ПРИЛОЖЕНИЕ ЗАКРЫЛОСЬ И ДАННЫЕ В БД ЗАПИСАЛИСЬ НЕ В ПОЛНОМ ОБЪЕМЕ
def deleter(air_time,ground_time):
    at_del = air_time
    gt = ground_time
    cur.execute("DELETE FROM air where time = :at_del",{"at_del": at_del})
    conn.commit()
    cur.execute("DELETE FROM ground WHERE time = :gt", {"gt": gt})
    conn.commit()


# ФУНКЦИЯ ЗАПРОСА ДАННЫХ ЗА ОПРЕДЕЛЕННЫЙ ПЕРИОД
def time_period(n):
    if isinstance(n, str):
        if n == '30min':
            cur.execute("SELECT * from air WHERE time BETWEEN  DATETIME('now','localtime','-30 minutes') and DATETIME('now','localtime')")
            air = cur.fetchall()
            cur.execute("SELECT * from ground WHERE time BETWEEN  DATETIME('now','localtime','-30 minutes') and DATETIME('now','localtime')")
            ground = cur.fetchall()
            final_result = perevod(air, ground)

        elif n == 'hour':
            cur.execute("SELECT * from air WHERE time BETWEEN  DATETIME('now','localtime','-1 hour') and DATETIME('now','localtime')")
            air = cur.fetchall()
            cur.execute("SELECT * from ground WHERE time BETWEEN  DATETIME('now','localtime','-1 hour') and DATETIME('now','localtime')")
            ground = cur.fetchall()
            final_result = perevod(air, ground)

        elif n == '12hours':
            cur.execute("SELECT * from air WHERE time BETWEEN  DATETIME('now','localtime','-12 hours') and DATETIME('now','localtime')")
            air = cur.fetchall()
            cur.execute("SELECT * from ground WHERE time BETWEEN  DATETIME('now','localtime','-12 hours') and DATETIME('now','localtime')")
            ground = cur.fetchall()
            final_result = perevod(air, ground)

        elif n == 'day':
            cur.execute("SELECT * from air WHERE time BETWEEN  DATETIME('now','localtime','-1 day') and DATETIME('now','localtime')")
            air = cur.fetchall()
            cur.execute("SELECT * from ground WHERE time BETWEEN  DATETIME('now','localtime','-1 day') and DATETIME('now','localtime')")
            ground = cur.fetchall()
            final_result = perevod(air, ground)

        elif n == 'week':
            cur.execute("SELECT * from air WHERE time BETWEEN  DATETIME('now','localtime','-1 week') and DATETIME('now','localtime')")
            air = cur.fetchall()
            cur.execute("SELECT * from ground WHERE time BETWEEN  DATETIME('now','localtime','-1 week') and DATETIME('now','localtime')")
            ground = cur.fetchall()
            final_result = perevod(air,ground)

        elif n == 'month':
            cur.execute("SELECT * FROM air WHERE time BETWEEN  DATETIME('now','localtime','-1 month') and DATETIME('now','localtime')")
            airq = cur.fetchall()
            cur.execute("SELECT * FROM ground WHERE time BETWEEN  DATETIME('now','localtime','-1 month') and DATETIME('now','localtime')")
            groundq = cur.fetchall()
            final_result = perevod(airq,groundq)
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
            id = int(var['data']['air'][i]['id'])
            temperature = float(var['data']['air'][i]['temperature'])
            humidity = float(var['data']['air'][i]['humidity'])
            time = var['timeAIR']
            aird = (result,id,temperature,humidity,time)
            cur.execute("INSERT INTO air VALUES(?, ?, ?, ?, ?);", aird)
            conn.commit()
            aird = ()
        else:
            result = str(var['data']['air'][i]['result'])
            id = int(var['data']['air'][i]['id'])
            temperature = 'null'
            humidity = 'null'
            time = var['timeAIR']
            aird = (result,id,temperature,humidity,time)
            cur.execute("INSERT INTO air VALUES(?, ?, ?, ?, ?);", aird)
            conn.commit()
            aird = ()
    # Запись в таблицу ground
    for i in range(0,6):
        if (str(var['data']['ground'][i]['result']) == 'True'):
            result = str(var['data']['ground'][i]['result'])
            id = int(var['data']['ground'][i]['id'])
            humidity = float(var['data']['ground'][i]['humidity'])
            time = var['timeGROUND']
            grd = (result,id,humidity,time)
            cur.execute("INSERT INTO ground VALUES(?, ?, ?, ?);", grd)
            conn.commit()
            grd = ()
        else:
            result = str(var['data']['ground'][i]['result'])
            id = int(var['data']['ground'][i]['id'])
            humidity = 'null'
            time = var['timeGROUND']
            grd = (result,id,humidity,time)
            cur.execute("INSERT INTO ground VALUES(?, ?, ?, ?);", grd)
            conn.commit()
            grd = ()


# ФУНКЦИЯ ПЕРЕВОДА ДАННЫХ ИЗ БД В ФОРМАТ JSON
def perevod(air_mas, ground_mas):
    ra = 0
    rg = 0
    result = ""
    result_air = ""
    result_ground = ""
    x = 0
    y = 0
    while ra < len(air_mas):
        dt = DT.datetime.strptime(air_mas[ra][4], '%Y-%m-%d %H:%M:%S')
        result_air += '{"dt": ' + str(int(dt.timestamp()) * 1000)
        for r in range(ra, ra+4):
            result_air += ',\n "t' + str(x+1) + '": ' + str(air_mas[r][2]) + ',\n "h' + str(x+1) + '": ' + str(air_mas[r][3])
            x += 1
        result_air += "},\n"
        ra += 4
        x = 0
    result_air = result_air[:-2]
    while rg < len(ground_mas):
        dtg = DT.datetime.strptime(ground_mas[rg][3], '%Y-%m-%d %H:%M:%S')
        result_ground += '{"dt": ' + str(int(dtg.timestamp()) * 1000)
        for r in range(rg, rg+6):
            result_ground += ',\n "h' + str(y+1) + '": ' + str(ground_mas[r][2])
            y += 1
        rg += 6
        y = 0
        result_ground += "},\n"
    result_ground = result_ground[:-2]
    result += "{\n\"air\": [\n" + result_air + "],\n\"ground\": [\n" + result_ground + "]}"
    return result


# ФУНКЦИЯ ПРОВЕРКИ ЦЕЛОСТНОСТИ ПОСЛЕДНЕЙ ЗАПИСИ (ВОЗМОЖНО ПРОГРАММА ПРЕКРАТИЛА РАБОТУ, НЕ УСПЕВ ЗАНЕСТИ ВСЕ ЗНАЧЕНИЯ В БД)
def proverka_last_data():
    cur.execute("SELECT * FROM air")
    last_air = cur.fetchall()
    cur.execute("SELECT * FROM ground")
    last_ground = cur.fetchall()
    if len(last_air) == len(last_ground) == 0:
        print('БД пуста')
        return False
    print(last_air[-1], last_air[-1][4])
    print(last_ground[-1], last_ground[-1][3])
    # ПРОВЕРКА НА НЕДОСТАЮЩИЕ ДАННЫЕ С ДАТЧИКОВ, КОТОРЫЕ МОГЛИ НЕДОПИСАТЬСЯ ВСЛЕДСТВИЕ ПРЕКРАЩЕНИЯ ПРОГРАММЫ
    if int(last_air[-1][1]) != 4 or int(last_ground[-1][1]) != 6:
        deleter(last_air[-1][4], last_ground[-1][3])
        print('Человечность данных восcтановлена!')
    else:
        print('С данными все хорошо!')


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


# ПРОВЕРЯЕМ НА ЦЕЛОСТНОСТЬ ПОСЛЕДНЕЙ ЗАПИСИ (4 ПОКАЗАНИЯ С ВОЗДУХА И 6 С ЗЕМЛИ)
proverka_last_data()


# ОБОЗНАЧЕНИЯ ПОТОКОВ
t1 = Thread(target=TEPLICA, args=())
t2 = Thread(target=SERVER, args=())


# ЗАПУСК ПОТОКОВ
t1.start()
t2.start()