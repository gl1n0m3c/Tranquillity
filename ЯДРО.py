import requests
import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import *
from time import *
import sqlite3
import datetime as DT
import json





#                                                                   БАЗА ДАННЫХ
# Ошибка неверного типа
err_Wrong_Type = 'wrong type'
# СОЗДАНИЕ ТАБЛИЦ AIR + GROUND
conn = sqlite3.connect('data.db', check_same_thread=False)
cur = conn.cursor()
# создание таблиц air, ground, last_parametr
cur.execute("""CREATE TABLE IF NOT EXISTS air(
   id INTEGER CHECK(id > 0 and id <=4),
   temperature REAL,
   humidity REAL,
   time TEXT,
   avg_temp REAL,
   avg_hum REAL
   );
""")
conn.commit()
cur.execute("""CREATE TABLE IF NOT EXISTS ground(
   id INTEGER CHECK(id > 0 and id <= 6),  
   humidity REAL,
   time TEXT);
""")
conn.commit()
cur.execute("""CREATE TABLE IF NOT EXISTS options(
    temperature REAL,
    air_hum REAL,
    gr_hum REAL);
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
    if(type(t) == int):
        t = float(t)
        cur.execute("UPDATE options SET temperature = :t", {"t": t})
        conn.commit()
    if(type(t) == float):
        cur.execute("UPDATE options SET temperature = :t",{"t": t})
        conn.commit()
    else:
        return err_Wrong_Type
    return ''


# ФУНКЦИЯ ОБНОВЛЕНИЯ ПОСЛЕДНЕГО ПАРАМЕТРА СРЕДНЕЙ  ВЛАЖНОСТИ ВОЗДУХА
def air_update(ah):
    if(type(ah) == int) and (ah <= 100) and (ah >= 0):
        ah = float(ah)
        cur.execute("UPDATE options SET air_hum = :ah", {"ah": ah})
        conn.commit()
        return ""
    if(type(ah) == float) and (ah <= 100) and (ah >= 0):
        cur.execute("UPDATE options SET air_hum = :ah", {"ah": ah})
        conn.commit()
        return ""
    else:
        return err_Wrong_Type


# ФУНКЦИЯ ОБНОВЛЕНИЯ ПОСЛЕДНЕГО ПАРАМЕТРА СРЕДНЕЙ ВЛАЖНОСТИ ЗЕМЛИ
def gr_update(gh):
    if(type(gh) == int) and (gh <= 100) and (gh >= 0):
        gh = float(gh)
        cur.execute("UPDATE options SET gr_hum = :gh", {"gh": gh})
        conn.commit()
        return ""
    if(type(gh) == float) and (gh <= 100) and (gh > 0):
        cur.execute("UPDATE options SET gr_hum = :gh", {"gh": gh})
        conn.commit()
        return ""
    else:
        return err_Wrong_Type


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
    if type(var) == dict:
        # запись в таблицу air
        try:
            time = dict_check(var, 'timeAIR', str)
            if var['AVGtemp'] is None:
                avg_temp = "null"
            else:
                avg_temp = dict_check(var, 'AVGtemp', float)
            if var['AVGhum'] is None:
                avg_hum = "null"
            else:
                avg_hum = dict_check(var, 'AVGhum', float)
            #запись в таблицу air
            for el in var['data']['air']:
                id = dict_check(el, 'id', int)
                if(el['temperature'] is None):
                    temperature = "null"
                else:
                    temperature = dict_check(el, 'temperature', (float))
                if(el['humidity'] is None):
                    humidity = "null"
                else:
                    humidity = dict_check(el, 'humidity', float)
                cur.execute("INSERT INTO air VALUES(?, ?, ?, ?, ?, ?);", (id, temperature, humidity, time, avg_temp, avg_hum))
            # Запись в таблицу ground
            time = dict_check(var, 'timeGROUND', str)
            for el in var['data']['ground']:
                id = dict_check(el, 'id', int)
                if (el['humidity'] is None):
                    humidity = "null"
                else:
                    humidity = dict_check(el, 'humidity', float)
                cur.execute("INSERT INTO ground VALUES(?, ?, ?);", (id, humidity, time))
            conn.commit()
        except Exception as e:
            conn.rollback()


# ФУНКЦИЯ ДОПОЛНИТЕЛЬНОЙ ПРОВЕРКИ
def dict_check(dict, name, type):
    if not (name in dict) or not isinstance(dict[name], type):
        raise Exception("Ошибка в параметре " + name)
    return dict[name]


# ФУНКЦИЯ ПЕРЕВОДА ДАННЫХ ИЗ БД В ФОРМАТ JSON
def perevod(air_mas, ground_mas):
    ra = 0
    rg = 0
    result = ""
    result_air = ""
    result_ground = ""
    x = 0
    y = 0
    if len(air_mas) == 0 or len(ground_mas) == 0:
        return "[]"
    while ra < len(air_mas):
        dt = DT.datetime.strptime(air_mas[ra][3], '%Y-%m-%d %H:%M:%S')
        avg_temp = air_mas[ra][4]
        avg_hum = air_mas[ra][5]
        result_air += '{"dt": ' + str(int(dt.timestamp()) * 1000) + ',\n "avg_temp": ' + str(avg_temp) + ',\n "avg_hum": ' + str(avg_hum)
        for r in range(ra, ra + 4):
            result_air += ',\n "t' + str(x + 1) + '": ' + str(air_mas[r][1]) + ',\n "h' + str(x + 1) + '": ' + str(
                air_mas[r][2])
            x += 1
        result_air += "},\n"
        ra += 4
        x = 0
    result_air = result_air[:-2]
    while rg < len(ground_mas):
        dtg = DT.datetime.strptime(ground_mas[rg][2], '%Y-%m-%d %H:%M:%S')
        result_ground += '{"dt": ' + str(int(dtg.timestamp()) * 1000)
        for r in range(rg, rg + 6):
            result_ground += ',\n "h' + str(y + 1) + '": ' + str(ground_mas[r][1])
            y += 1
        rg += 6
        y = 0
        result_ground += "},\n"
    result_ground = result_ground[:-2]
    result += "{\n\"air\": [\n" + result_air + "],\n\"ground\": [\n" + result_ground + "]}"
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
        data_per_5sec = {'timeAIR': 0, 'timeGROUND': 0, 'AVGtemp': None, 'AVGhum': None, 'data': {'air': [], 'ground': []}}
        # Время начала отправки первого запроса в UNIX
        T1_1 = datetime.datetime.now()
        T1_1 = (T1_1 - datetime.datetime(1970, 1, 1)).total_seconds()
        # Создание цикла с обращениями к серверу (температура + влажность воздуха)
        for i in range(1, 5):
            try:
                k = requests.get(URL_Temperature_AirHumidity + str(i), timeout=timeout_for_sensors)
            except Exception:
                data_per_5sec['data']['air'].append({'id': i, 'temperature': None, 'humidity': None})
            else:
                count += 1
                sr_temp += k.json()['temperature']
                sr_humidity_AIR += k.json()['humidity']
                data_per_5sec['data']['air'].append(
                    {'id': i, 'temperature': k.json()['temperature'], 'humidity': k.json()['humidity']})
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
                data_per_5sec['data']['ground'].append({'id': i, 'humidity': None})
                last_GROUND_humidity[i - 1] = None
            else:
                last_GROUND_humidity[i - 1] = (k.json()['humidity'])
                data_per_5sec['data']['ground'].append({'id': i, 'humidity': k.json()['humidity']})
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
        # Приведение средних параметров в нормальное состояние))
        if count != 0:
            sr_humidity_AIR = round(sr_humidity_AIR / count, 2)
            sr_temp = round(sr_temp / count, 2)
        else:
            sr_temp = None
            sr_humidity_AIR = None
        # Добавление времени и срелних показателей
        data_per_5sec['timeAIR'] = T1
        data_per_5sec['timeGROUND'] = T2
        data_per_5sec['AVGtemp'] = sr_temp
        data_per_5sec['AVGhum'] = sr_humidity_AIR
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
            global extreme_mode
            # Основные настройки сервера
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            # Массив, в котором хранятятся данные, переданные пользователем через ссылку
            m = self.path[1:].split('/')
            # УВЕДОМЛЕНИЕ О ЗАПУСКЕ ИЛИ ОБНОВЛЕНИИ ПОЛЬЗОВАТЕЛЬСКОГО ИНТЕРФЕЙСА
            if m[0] == 'update':
                # Закрытие форточек
                try:
                    k = requests.patch(url='https://dt.miet.ru/ppo_it/api/fork_drive', params={"state": 0})
                except Exception:
                    self.wfile.write("{\"message\": \"Сервер теплицы не отвечает!\"}".encode())
                else:
                    self.wfile.write("{\"message\": \"Форточка закрыта!\"}".encode())
                # Выключение системы увлажнения воздуха
                try:
                    k = requests.patch(url='https://dt.miet.ru/ppo_it/api/total_hum', params={"state": 0})
                except Exception:
                    self.wfile.write("{\"message\": \"Сервер теплицы не отвечает!\"}".encode())
                else:
                    self.wfile.write("{\"message\": \"Система увлажнения воздуха выключена!\"}".encode())
                # Выключение систем увлажнения бороздок
                for i in range(1, 7):
                    try:
                        k = requests.patch(url='https://dt.miet.ru/ppo_it/api/watering',
                                           params={"id": i, "state": 0})
                    except Exception:
                        self.wfile.write("{\"message\": \"Сервер теплицы не отвечает!\"}".encode())
                    else:
                        self.wfile.write("{\"message\": \"Система полива бороздки выключена!\"}".encode())

            # ЗАПРОС НА ВКЛЮЧЕНИЕ ЭКСТРЕННОГО РЕЖИМА
            elif m[0] == 'on_extreme_mode':
                extreme_mode = True

            # ЗАПРОС НА ВЫКЛЮЧЕНИЕ ЭКСТРЕННОГО РЕЖИМА
            elif m[0] == 'off_extreme_mode':
                extreme_mode = False
            # ЗАПРОС НА СОХРАНЕНИЕ ДАННЫХ С ПОЛЬЗОВАТЕЛЬСКОГО ИНТЕРФЕЙСА
            elif m[0] == 'save':
                global sr_temp
                global sr_humidity_AIR
                global last_GROUND_humidity
                # Определение времени
                timenow = str(datetime.datetime.now())[:-7]
                # Структуры, которая будет передоваться в функцию table_append
                data = {'timeAIR': timenow, 'timeGROUND': timenow, 'AVGtemp': None, 'AVGhum': None,  'data': {'air': [], 'ground': []}}
                # Счётчики температур и влажностей
                count_temp = 0
                count_hum = 0
                # Суммы температур и влажностей
                sum_temp = 0
                sum_hum = 0
                # Заполнение структуры данными
                for i in range(1, 5):
                    if m[i] == '':
                        temp = None
                    else:
                        temp = float(m[i])
                        count_temp += 1
                        sum_temp += temp
                    if m[i + 4] == '':
                        hum = None
                    else:
                        hum = float(m[i + 4])
                        count_hum += 1
                        sum_hum += hum
                    data['data']['air'].append({'id': i, 'temperature': temp, 'humidity': hum})

                for i in range(9, 15):
                    if m[i] == '':
                        ground_hum = None
                    else:
                        ground_hum = float(m[i])
                    data['data']['ground'].append({'id': i - 8, 'humidity': ground_hum})
                    last_GROUND_humidity[i - 9] = ground_hum

                if count_temp != 0:
                    data['AVGtemp'] = round(sum_temp / count_temp, 2)
                    sr_temp = round(sum_temp / count_temp, 2)
                else:
                    sr_temp = None
                if count_hum != 0:
                    data['AVGhum'] = round(sum_hum / count_hum, 2)
                    sr_humidity_AIR = round(sum_hum / count_hum, 2)
                else:
                    sr_humidity_AIR = None

                # Сохранение данных в БД
                table_append(data)

            # СОХРАНЕНИЕ ПОСЛЕДНЕГО ПАРАМЕТРА СРЕДНЕЙ ТЕМПЕРАТУРЫ ВОЗДУХА
            elif m[0] == 'clean_db':
                null()

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

            # ЗАПРОС НА ПЕРЕДАЧУ ПОСЛЕДНИХ НАСТРОЕК ПОЛЬЗОВАТЕЛЯ
            elif m[0] == 'give_options':
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

            # ПРОВЕРКА НА ВОЗМОЖНОСТЬ ОТКРЫТИЯ ФОРТОЧКИ (ЭКСТРЕННЫЙ РЕЖИМ / НЕОПРЕДЕЛЕННЫЙ СРЕДНИЙ ПОКАЗАТЕЛЬ)
            elif m[0] == 'open_windows' and (extreme_mode == True or sr_temp == None):
                try:
                    k = requests.patch(url='https://dt.miet.ru/ppo_it/api/fork_drive', params={"state": 1})
                except Exception:
                    self.wfile.write("{\"message\": \"Сервер теплицы не отвечает!\"}".encode())
                else:
                    self.wfile.write("{\"message\": \"Форточка открыта!\"}".encode())

            # ПРОВЕРКА НА ВОЗМОЖНОСТЬ ОТКРЫТИЯ ФОРТОЧКИ
            elif m[0] == 'open_windows' and extreme_mode == False:
                cur.execute("SELECT temperature, air_hum, gr_hum from options")
                axc = cur.fetchall()
                if len(axc) == 0:
                    try:
                        k = requests.patch(url='https://dt.miet.ru/ppo_it/api/fork_drive', params={"state": 1})
                    except Exception:
                        self.wfile.write("{\"message\": \"Сервер теплицы не отвечает!\"}".encode())
                    else:
                        self.wfile.write("{\"message\": \"Форточка открыта!\"}".encode())
                elif axc[0][0] < sr_temp:
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

            # ПРОВЕРКА НА ВОЗМОЖНОСТЬ ВКЛЮЧЕНИЯ СИСТЕМЫ УВЛАЖНЕНИЯ ВОЗДУХА В ТЕПЛИЦЕ (ЭКСТРЕННЫЙ РЕЖИМ / НЕОПРЕДЕЛЕННЫЙ СРЕДНИЙ ПОКАЗАТЕЛЬ)
            elif m[0] == 'start_humidity_system' and (extreme_mode == True or sr_humidity_AIR == None):
                try:
                    k = requests.patch(url='https://dt.miet.ru/ppo_it/api/total_hum', params={"state": 1})
                except Exception:
                    self.wfile.write("{\"message\": \"Сервер теплицы не отвечает!\"}".encode())
                else:
                    self.wfile.write("{\"message\": \"Система увлажнения включена!\"}".encode())

            # ПРОВЕРКА НА ВОЗМОЖНОСТЬ ВКЛЮЧЕНИЯ СИСТЕМЫ УВЛАЖНЕНИЯ ВОЗДУХА В ТЕПЛИЦЕ
            elif m[0] == 'start_humidity_system' and extreme_mode == False:
                cur.execute("SELECT temperature, air_hum, gr_hum from options")
                axc = cur.fetchall()
                if len(axc) == 0:
                    try:
                        k = requests.patch(url='https://dt.miet.ru/ppo_it/api/total_hum', params={"state": 1})
                    except Exception:
                        self.wfile.write("{\"message\": \"Сервер теплицы не отвечает!\"}".encode())
                    else:
                        self.wfile.write("{\"message\": \"Система увлажнения включена!\"}".encode())
                if axc[0][1] > sr_humidity_AIR:
                    try:
                        k = requests.patch(url='https://dt.miet.ru/ppo_it/api/total_hum', params={"state": 1})
                    except Exception:
                        self.wfile.write("{\"message\": \"Сервер теплицы не отвечает!\"}".encode())
                    else:
                        self.wfile.write("{\"message\": \"Система увлажнения включена!\"}".encode())
                else:
                    self.wfile.write("{\"message\": \"Система увлажнения воздуха не может быть включена в связи с избыточной влажностью в теплице!\"}".encode())

            # ПРОВЕРКА НА ВОЗМОЖНОСТЬ ВЫКЛЮЧЕНИЯ СИСТЕМЫ УВЛАЖНЕНИЯ ВОЗДУХА В ТЕПЛИЦЕ
            elif m[0] == 'stop_humidity_system':
                try:
                    k = requests.patch(url='https://dt.miet.ru/ppo_it/api/total_hum', params={"state": 0})
                except Exception:
                    self.wfile.write("{\"message\": \"Сервер теплицы не отвечает!\"}".encode())
                else:
                    self.wfile.write("{\"message\": \"Система увлажнения воздуха выключена!\"}".encode())

            # ПРОВЕРКА НА ВОЗМОЖНОСТЬ НАЧАЛА ПОЛИВА КОНКРЕТНОЙ БОРОЗДКИ (ЭКСТРЕННЫЙ РЕЖИМ / НЕОПРЕДЕЛЕННЫЙ СРЕДНИЙ ПОКАЗАТЕЛЬ)
            elif m[0] == 'start_wattering' and (extreme_mode == True or last_GROUND_humidity[(int(m[1])) - 1] == None):
                try:
                    k = requests.patch(url='https://dt.miet.ru/ppo_it/api/watering',
                                       params={"id": int(m[1]), "state": 1})
                except Exception:
                    self.wfile.write("{\"message\": \"Сервер теплицы не отвечает!\"}".encode())
                else:
                    self.wfile.write("{\"message\": \"Система полива бороздки включена!\"}".encode())

            # ПРОВЕРКА НА ВОЗМОЖНОСТЬ НАЧАЛА ПОЛИВА КОНКРЕТНОЙ БОРОЗДКИ
            elif m[0] == 'start_wattering' and extreme_mode == False:
                cur.execute("SELECT temperature, air_hum, gr_hum from options")
                axc = cur.fetchall()
                if len(axc) == 0:
                    try:
                        k = requests.patch(url='https://dt.miet.ru/ppo_it/api/watering',
                                           params={"id": int(m[1]), "state": 1})
                    except Exception:
                        self.wfile.write("{\"message\": \"Сервер теплицы не отвечает!\"}".encode())
                    else:
                        self.wfile.write("{\"message\": \"Система полива бороздки включена!\"}".encode())
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

            # ИНАЧЕ
            else:
                self.wfile.write("{\"message\": \"Неверная ссылка!\"}".encode())

    # Параметры сервера
    port = 27314
    server_addres = ('', port)
    httpd = ThreadingHTTPServer(server_addres, HttpGetHandler)
    httpd.serve_forever()


# Режим экстренного управления (изначально выключен)
extreme_mode = False


# ОБОЗНАЧЕНИЯ ПОТОКОВ
t1 = Thread(target=TEPLICA, args=())
t2 = Thread(target=SERVER, args=())


# ЗАПУСК ПОТОКОВ
t1.start()
t2.start()