import json
import sqlite3
conn = sqlite3.connect('data.db')
cur = conn.cursor()
# def perevod(air_mas, ground_mas):
#     ra = 0
#     rg = 0
#     result = '{"DATA": [\n'
#     while ra < len(air_mas):
#         result += "{'timeAIR':" + air_mas[ra][4] + ",'timeGROUND':" + ground_mas[rg][3] + ",'data':{\n'air': ["
#         for r in range(ra,ra+4):
#             result += "{'result': " + air_mas[r][0] + ",'id': "       + air_mas[r][1] + ",'temperature': " + \
#                                       air_mas[r][2] + ",'humidity': " + air_mas[r][3] + "},\n"
#         ra += 4
#         result += "],\n'ground': [\n"
#         for r in range(rg,rg+6):
#             result += "{'result': " + ground_mas[r][0] + ",'id': " + ground_mas[r][1] + ",'humidity': " + ground_mas[r][2] + "},\n"
#         rg += 6
#         result += "]}},\n"
#     result += "]}"
#     return result
def perevod(air_mas, ground_mas):
    ra = 0
    rg = 0
    result = ""
    result_air = ""
    result_ground = ""
    x = 0
    y = 0
    while ra < len(air_mas):
        result_air += '{"dt": ' + str(air_mas[ra][4])
        for r in range(ra,ra+4):
            result_air += ',\n "t' + str(x+1) + '": ' + str(air_mas[r][2]) + ',\n "h' + str(x+1) + '": ' + str(air_mas[r][3])
            x+=1
        result_air += "},\n"
        ra += 4
        x = 0

    while rg < len(ground_mas):
        result_ground += '{"dt": ' + str(ground_mas[rg][3])
        for r in range(rg,rg+6):
            result_ground += ',\n "h' + str(y+1) + '": ' + str(ground_mas[r][2])
            y+=1
        rg += 6
        y = 0
        result_ground += "},\n"
    result += "{\nair: [\n" + result_air + "],\nground: [\n" + result_ground + "]}"
    return result
def break_delete(air_time,ground_time):
    at_del = air_time
    gt = ground_time
    cur.execute("DELETE FROM newair where time = :at_del",{"at_del": at_del})
    conn.commit()
    cur.execute("DELETE FROM newground WHERE time = :gt", {"gt": gt})
    conn.commit()
#создание таблиц air, ground, last_parametr
cur.execute("""CREATE TABLE IF NOT EXISTS air(
   result TEXT,
   id INTEGER,
   temperature REAL,
   humidity REAL,
   time INTEGER);
""")
conn.commit()
cur.execute("""CREATE TABLE IF NOT EXISTS ground(
   result TEXT,
   id INTEGER,  
   humidity REAL,
   time INTEGER);
""")
conn.commit()
cur.execute("""CREATE TABLE IF NOT EXISTS options(
    temperature INTEGER,
    air_hum INTEGER,
    gr_hum INTEGER);
""")
conn.commit()
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

    for i in range(0,4):
        print("pizda")
        if (str(var['data']['air'][i]['result']) == 'True'):
            result = str(var['data']['air'][i]['result'])
            id = int(var['data']['air'][i]['id'])
            temperature = float(var['data']['air'][i]['temperature'])
            humidity = float(var['data']['air'][i]['humidity'])
            time = int(var['timeAIR'])
            aird = (result,id,temperature,humidity,time)
            cur.execute("INSERT INTO air VALUES(?, ?, ?, ?, ?);", aird)
            conn.commit()
            aird = ()
            print("dildo")
        else:
            print("zhopa")
            result = str(var['data']['air'][i]['result'])
            id = int(var['data']['air'][i]['id'])
            temperature = 'null'
            humidity = 'null'
            time = int(var['timeAIR'])
            aird = (result,id,temperature,humidity,time)
            cur.execute("INSERT INTO air VALUES(?, ?, ?, ?, ?);", aird)
            conn.commit()
            aird = ()

        #запись в таблицу ground
    for i in range(0,6):
        print("penis")
        if (str(var['data']['ground'][i]['result']) == 'True'):
            print("anal")
            result = str(var['data']['ground'][i]['result'])
            id = int(var['data']['ground'][i]['id'])
            humidity = float(var['data']['ground'][i]['humidity'])
            time = int(var['timeGROUND'])
            grd = (result,id,humidity,time)
            cur.execute("INSERT INTO ground VALUES(?, ?, ?, ?);", grd)
            conn.commit()
            grd = ()
        else:
            print("churban")
            result = str(var['data']['ground'][i]['result'])
            id = int(var['data']['ground'][i]['id'])
            humidity = 'null'
            time = int(var['timeGROUND'])
            grd = (result,id,humidity,time)
            cur.execute("INSERT INTO ground VALUES(?, ?, ?, ?);", grd)
            conn.commit()
            grd = ()

# # #удаление
# cur.execute("DELETE FROM newair;")
# conn.commit()
# cur.execute("DELETE FROM newground;")
# conn.commit()
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
            cur.execute("SELECT * FROM air")
            airq = cur.fetchall()
            cur.execute("SELECT * FROM ground")
            groundq = cur.fetchall()
            print(airq)
            print(groundq)
            final_result = perevod(airq,groundq)


        else:
            return "Неизвестная дата"
        return final_result
    else:
        return "Неверный формат"
table_append(var3)
cur.execute("SELECT * FROM air")
air = cur.fetchall()
cur.execute("SELECT * FROM ground")
ground = cur.fetchall()
print(air)
print(ground)
print(time_period('month'))
