import json
import sqlite3
import datetime as DT
from time import *
conn = sqlite3.connect('data.db')
cur = conn.cursor()
# def perevod(air_mas, ground_mas):

err_Wrong Type = 'wrong type'
def perevod(air_mas, ground_mas):
    ra = 0
    rg = 0
    result = ""
    result_air = ""
    result_ground = ""
    x = 0
    y = 0
    #if(type)
    if len(air_mas) == 0 or len(ground_mas) == 0:
        return "no data"
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
   id INTEGER CHECK(id > 0 and id <=4),
   temperature REAL,
   humidity REAL,
   time TEXT
   );
""")
conn.commit()
cur.execute("""CREATE TABLE IF NOT EXISTS ground(
   result TEXT,
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
cur.execute("""CREATE TABLE IF NOT EXISTS test_air(
   result TEXT,
   id INTEGER CHECK(id > 0 and id <=4),
   temperature REAL,
   humidity REAL,
   time TEXT
   );
""")
conn.commit()
cur.execute("""CREATE TABLE IF NOT EXISTS test_ground(
   result TEXT,
   id INTEGER CHECK(id > 0 and id <= 6),  
   humidity REAL,
   time TEXT);
""")
conn.commit()
cur.execute("""CREATE TABLE IF NOT EXISTS test_options(
    temperature REAL,
    air_hum REAL,
    gr_hum REAL);
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
def ttemp_update(t):
    if(type(t) == float):
        cur.execute("UPDATE options SET temperature = :t",{"t": t})
        conn.commit()
    else:
        return "wrong type"

def tair_update(ah):
    if(type(ah) == float) and (ah <= 100) and (ah > 0):
        cur.execute("UPDATE options SET air_hum = :ah", {"ah": ah})
        conn.commit()
        return ""
    else:
        return err_Wrong_Type
def tgr_update(gh):
    if(type(gh) == float):
        #if(gh > 100 or):
        cur.execute("UPDATE options SET gr_hum = :gh", {"gh": gh})
        conn.commit()
    else:
        return err_Wrong_Type










def selftest_option():
    if (tair_update(0.0) != err_Wrong_Type) or \
       (tair_update(100.0001) != err_Wrong_Type) or \
       (tair_update("0.0") != err_Wrong_Type) or (tair_update(int(12)) != err_Wrong_Type):
        raise Exception('Ошибка самопроверки - tair_update')
    if tair_update(0.0001) == '':
        cur.execute("SELECT gr_hum FROM options;")
        a = cur.fetchall()
        if len(a)
    if tair_update(100.0) == '':
selftest_option()

def tstart_options():
    cur.execute("SELECT * FROM test_options")
    axc = cur.fetchall()
    if len(axc) == 0:
        cur.execute("INSERT INTO test_options VALUES (?,?,?)", (0,0,0))
        conn.commit()
    else:
        return
def temp_update(t):
    cur.execute("UPDATE test_options SET temperature = :t",{"t": t})
    conn.commit()

def air_update(ah):
    cur.execute("UPDATE test_options SET air_hum = :ah", {"ah": ah})
    conn.commit()
def gr_update(gh):
    cur.execute("UPDATE test_options SET gr_hum = :gh", {"gh": gh})
    conn.commit()

tstart_options()
ttemp_update(31)
tair_update(32)
tgr_update(48)
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
           'air': [
               {'result': False, 'id': 1},
               {'result': True, 'id': 2, 'temperature': 12.12, 'humidity': 63.43},
               {'result': False, 'id': 3},
               {'result': False, 'id': 4}],
           'ground': [{
               'result': False, 'id': 1},
               {'result': True, 'id': 2, 'humidity': 66.4},
               {'result': False, 'id': 3},
               {'result': True, 'id': 4, 'humidity': 70.94},
               {'result': False, 'id': 5},
               {'result': False, 'id': 6}]}}
print(type(var2))
print(len(var2['data']['ground']))



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
var3 = {'timeAIR': 1675711739,
        'timeGROUND': 1675711741,
        'data': {
            'air': [
                {'result': True, 'id': 1, 'temperature': 32.29, 'humidity': 73.21},
                {'result': True, 'id': 2, 'temperature': 31.21, 'humidity': 71.9},
                {'result': True, 'id': 3, 'temperature': 29.22, 'humidity': 57.26},
                {'result': True, 'id': 4, 'temperature': 29.78, 'humidity': 46.96}],
            'ground': [
                {'result': True, 'id': 1, 'humidity': 23.21},
                {'result': True, 'id': 2, 'humidity': 73.17},
                {'result': True, 'id': 3, 'humidity': 67.58},
                {'result': True, 'id': 4, 'humidity': 64.8},
                {'result': True, 'id': 5, 'humidity': 74.02},
                {'result': True, 'id': 6, 'humidity': 71.62}]}}
print(type(var3['data']['air'][0]['result']))

def dict_check(dict, name, type):
    if not (name in dict) or not isinstance(dict[name], type):
        raise Exception("Ошибка в параметре " + name)
    print(dict[name], name, type)
    return dict[name]
def t_table_append(var):
    if type(var) == dict:
        # запись в таблицу air
        try:
            time = dict_check(var, 'timeAIR', str)
            #запись в таблицу air
            for el in var['data']['air']:
                #print(el)
                res = str(dict_check(el, 'result', bool))
                id = dict_check(el, 'id', int)
                if (el['result']):
                    temperature = dict_check(el, 'temperature', float)
                    humidity = dict_check(el, 'humidity', float)
                else:
                    temperature = 'null'
                    humidity = 'null'
                cur.execute("INSERT INTO test_air VALUES(?, ?, ?, ?, ?);", (res,id,temperature,humidity,time))
            #запись в таблицу ground
            time = dict_check(var, 'timeGROUND', str)
            for el in var['data']['ground']:
                res = str(dict_check(el, 'result', bool))
                id = dict_check(el, 'id', int)
                if (el['result']):
                    humidity = dict_check(el, 'humidity', float)
                else:
                    humidity = 'null'
                cur.execute("INSERT INTO test_ground VALUES(?, ?, ?, ?);", (res,id,humidity,time))
            conn.commit()
        except Exception as e:
            print("Ошибка - " + str(e))
            conn.rollback()
# # #удаление
def null1():
    cur.execute("DELETE FROM test_air;")
    conn.commit()
    cur.execute("DELETE FROM test_ground;")
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
def ttime_period(n):
    if isinstance(n, str):
        if n == '30min':
            cur.execute("SELECT * from test_air WHERE time BETWEEN  DATETIME('now','localtime','-30 minutes') and DATETIME('now','localtime')")
            air = cur.fetchall()
            cur.execute("SELECT * from test_ground WHERE time BETWEEN  DATETIME('now','localtime','-30 minutes') and DATETIME('now','localtime')")
            ground = cur.fetchall()
            final_result = perevod(air, ground)

        elif n == 'hour':
            cur.execute("SELECT * from test_air WHERE time BETWEEN  DATETIME('now','localtime','-1 hour') and DATETIME('now','localtime')")
            air = cur.fetchall()
            cur.execute("SELECT * from test_ground WHERE time BETWEEN  DATETIME('now','localtime','-1 hour') and DATETIME('now','localtime')")
            ground = cur.fetchall()
            final_result = perevod(air, ground)

        elif n == '12hours':
            cur.execute("SELECT * from test_air WHERE time BETWEEN  DATETIME('now','localtime','-12 hours') and DATETIME('now','localtime')")
            air = cur.fetchall()
            cur.execute("SELECT * from test_ground WHERE time BETWEEN  DATETIME('now','localtime','-12 hours') and DATETIME('now','localtime')")
            ground = cur.fetchall()
            final_result = perevod(air, ground)

        elif n == 'day':
            cur.execute("SELECT * from test_air WHERE time BETWEEN  DATETIME('now','localtime','-1 day') and DATETIME('now','localtime')")
            air = cur.fetchall()
            cur.execute("SELECT * from test_ground WHERE time BETWEEN  DATETIME('now','localtime','-1 day') and DATETIME('now','localtime')")
            ground = cur.fetchall()
            final_result = perevod(air, ground)

        elif n == 'week':
            cur.execute("SELECT * from test_air WHERE time BETWEEN  DATETIME('now','localtime','-1 week') and DATETIME('now','localtime')")
            air = cur.fetchall()
            cur.execute("SELECT * from test_ground WHERE time BETWEEN  DATETIME('now','localtime','-1 week') and DATETIME('now','localtime')")
            ground = cur.fetchall()
            final_result = perevod(air,ground)

        elif n == 'month':
            cur.execute("SELECT * FROM test_air WHERE time BETWEEN  DATETIME('now','localtime','-1 month') and DATETIME('now','localtime')")
            airq = cur.fetchall()
            cur.execute("SELECT * FROM test_ground WHERE time BETWEEN  DATETIME('now','localtime','-1 month') and DATETIME('now','localtime')")
            groundq = cur.fetchall()
            final_result = perevod(airq,groundq)


        else:
            return "Неизвестная дата"
        return final_result
    else:
        return "Неверный формат"
print(t_table_append(var2))

#null1()
print(ttime_period('month'))
