import json
import sqlite3
import datetime as DT
from time import *
conn = sqlite3.connect('data.db')
cur = conn.cursor()
# def perevod(air_mas, ground_mas):

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

        result_air += '{"dt": ' + str(dt.timestamp())
        for r in range(ra,ra+4):
            result_air += ',"t' + str(x+1) + '": ' + str(air_mas[r][2]) + ',"h' + str(x+1) + '": ' + str(air_mas[r][3])
            x+=1
        result_air += "},\n"
        ra += 4
        x = 0
    result_air = result_air[:-2]
    while rg < len(ground_mas):
        dtg = DT.datetime.strptime(ground_mas[rg][3], '%Y-%m-%d %H:%M:%S')
        result_ground += '{"dt": ' + str(dtg.timestamp())
        for r in range(rg,rg+6):
            result_ground += ',"h' + str(y+1) + '": ' + str(ground_mas[r][2])
            y+=1
        rg += 6
        y = 0
        result_ground += "},\n"
    result_ground = result_ground[:-2]
    result += "{\nair: [\n" + result_air + "],\nground: [\n" + result_ground + "]}"
    return result
def break_delete(air_time,ground_time):
    at_del = air_time
    gt = ground_time
    cur.execute("DELETE FROM air where time = :at_del",{"at_del": at_del})
    conn.commit()
    cur.execute("DELETE FROM ground WHERE time = :gt", {"gt": gt})
    conn.commit()
#создание таблиц air, ground, last_parametr
cur.execute("""CREATE TABLE IF NOT EXISTS air(
   result TEXT,
   id INTEGER,
   temperature REAL,
   humidity REAL,
   time TEXT
   );
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
# time,id,type,result,
def start_options():
    cur.execute("SELECT * FROM options")
    axc = cur.fetchall()
    if len(axc) == 0:
        cur.execute("INSERT INTO options VALUES (?,?,?)", (0,0,0))
        conn.commit()
    else:
        return
def temp_update(t):
    cur.execute("UPDATE options SET temperature = :t",{"t": t})
    conn.commit()

def air_update(ah):
    cur.execute("UPDATE options SET air_hum = :ah", {"ah": ah})
    conn.commit()
def gr_update(gh):
    cur.execute("UPDATE options SET gr_hum = :gh", {"gh": gh})
    conn.commit()

start_options()
temp_update(31)
air_update(32)
gr_update(48)
#работа с кортежами для занесения данных в таблицу
var1 = {'timeAIR': '2023-01-22 13:24:07',
       'timeGROUND': '2023-01-22 13:24:08',
       'data': {
           'air': [{
               'result': False, 'id': 1},
               {'result': True, 'id': 2, 'temperature': 29.2, 'humidity': 63.43},
               {'result': False, 'id': 3},
               {'result': False, 'id': 4}],
           'ground': [{
               'result': False, 'id': 1},
               {'result': True, 'id': 2, 'humidity': 66.4},
               {'result': False, 'id': 3},
               {'result': True, 'id': 4, 'humidity': 70.94},
               {'result': False, 'id': 5},
               {'result': False, 'id': 6}]}}

var2 = {'timeAIR': '2023-01-22 13:24:07',
       'timeGROUND': '2023-01-22 13:24:08',
       'data': {
           'air': [{
               'result': False, 'id': 1},
               {'result': True, 'id': 2, 'temperature': 29.2, 'humidity': 63.43},
               {'result': False, 'id': 3},
               {'result': False, 'id': 4}],
           'ground': [{
               'result': False, 'id': 1},
               {'result': True, 'id': 2, 'humidity': 66.4},
               {'result': False, 'id': 3},
               {'result': True, 'id': 4, 'humidity': 70.94},
               {'result': False, 'id': 5},
               {'result': False, 'id': 6}]}}
print(len(var2['data']['air']))
print(len(var2['data']['ground']))
var3 = {'timeAIR': 1675711739,
        'timeGROUND': 1675711741,
        'data': {
            'air': [
                {'result': True, 'id': 1, 'temperature': 32.29, 'humidity': 73.21},
                {'result': True, 'id': 2, 'temperature': 31.21, 'humidity': 71.9},
                {'result': True, 'id': 3, 'temperature': 29.22, 'humidity': 57.26},
                {'result': True, 'id': 4, 'temperature': 29.78, 'humidity': 46.96}],
            'ground': [
                {'result': True, 'id': 1, 'humidity': 69.75},
                {'result': True, 'id': 2, 'humidity': 73.17},
                {'result': True, 'id': 3, 'humidity': 67.58},
                {'result': True, 'id': 4, 'humidity': 64.8},
                {'result': True, 'id': 5, 'humidity': 74.02},
                {'result': True, 'id': 6, 'humidity': 71.62}]}}


def table_append(var):
    # запись в таблицу air
    try:
        for i in range(0,4):
            if (str(var['data']['air'][i]['result']) == 'True'):
                result = str(var['data']['air'][i]['result'])
                id = int(var['data']['air'][i]['id'])
                temperature = float(var['data']['air'][i]['temperature'])
                humidity = float(var['data']['air'][i]['humidity'])
                time = var['timeAIR']
                aird = (result,id,temperature,humidity,time)

                cur.execute("INSERT INTO air VALUES(?, ?, ?, ?, ?);", aird)
                    # conn.commit()
                aird = ()
            else:
                result = str(var['data']['air'][i]['result'])
                id = int(var['data']['air'][i]['id'])
                temperature = 'null'
                humidity = 'null'
                time = var['timeAIR']
                aird = (result,id,temperature,humidity,time)
                cur.execute("INSERT INTO air VALUES(?, ?, ?, ?, ?);", aird)
            #    conn.commit()
                aird = ()

        #запись в таблицу ground
        for i in range(0,6):

            if (str(var['data']['ground'][i]['result']) == 'True'):
                result = str(var['data']['ground'][i]['result'])
                id = int(var['data']['ground'][i]['id'])
                humidity = float(var['data']['ground'][i]['humidity'])
                time = var['timeGROUND']
                grd = (result,id,humidity,time)
                cur.execute("INSERT INTO ground VALUES(?, ?, ?, ?);", grd)
                    # conn.commit()
                grd = ()
            else:
                result = str(var['data']['ground'][i]['result'])
                id = int(var['data']['ground'][i]['id'])
                humidity = 'null'
                time = var['timeGROUND']
                grd = (result,id,humidity,time)
                cur.execute("INSERT INTO ground VALUES(?, ?, ?, ?);", grd)
                grd = ()
        conn.commit()
    except GeneratorExit as e:
        print("error")
        conn.rollback()
# def table_append(var):
#     # запись в таблицу air
#
#     for i in range(0,4):
#         if (str(var['data']['air'][i]['result']) == 'True'):
#             result = str(var['data']['air'][i]['result'])
#             id = int(var['data']['air'][i]['id'])
#             temperature = float(var['data']['air'][i]['temperature'])
#             humidity = float(var['data']['air'][i]['humidity'])
#             time = var['timeAIR']
#             aird = (result,id,temperature,humidity,time)
#             try:
#                 cur.execute("INSERT INTO air VALUES(?, ?, ?, ?, ?);", aird)
#                 conn.commit()
#             except sqlite3.Error:
#                 conn.rollback()
#             aird = ()
#         else:
#             result = str(var['data']['air'][i]['result'])
#             id = int(var['data']['air'][i]['id'])
#             temperature = 'null'
#             humidity = 'null'
#             time = var['timeAIR']
#             aird = (result,id,temperature,humidity,time)
#             try:
#                 cur.execute("INSERT INTO air VALUES(?, ?, ?, ?, ?);", aird)
#                 conn.commit()
#             except sqlite3.Error:
#                 conn.rollback()
#             aird = ()
#
#         #запись в таблицу ground
#     for i in range(0,6):
#
#         if (str(var['data']['ground'][i]['result']) == 'True'):
#             result = str(var['data']['ground'][i]['result'])
#             id = int(var['data']['ground'][i]['id'])
#             humidity = float(var['data']['ground'][i]['humidity'])
#             time = var['timeGROUND']
#             grd = (result,id,humidity,time)
#             cur.execute("INSERT INTO ground VALUES(?, ?, ?, ?);", grd)
#             conn.commit()
#             grd = ()
#         else:
#             result = str(var['data']['ground'][i]['result'])
#             id = int(var['data']['ground'][i]['id'])
#             humidity = 'null'
#             time = var['timeGROUND']
#             grd = (result,id,humidity,time)
#             cur.execute("INSERT INTO ground VALUES(?, ?, ?, ?);", grd)
#             conn.commit()
#             grd = ()

# # #удаление
cur.execute("DELETE FROM air;")
conn.commit()
cur.execute("DELETE FROM ground;")
conn.commit()
# #вывод данных за определённый промежуток(минута, 10 минут, 30 минут, 1 час, 12 часов, 1 день, 1 месяц)

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
table_append(var2)
table_append(var1)
print(time_period('month'))
