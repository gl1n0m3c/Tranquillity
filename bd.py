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
        result_air += "{dt:" + air_mas[ra][4]
        for r in range(ra,ra+4):
            result_air += ", t" + str(x+1) + ":" + air_mas[r][2] + ", h" + str(x+1) + ":" + air_mas[r][3]
            x+=1
        result_air += "},\n"
        ra += 4
        x = 0

    while rg < len(ground_mas):
        result_ground += "{dt:" + ground_mas[rg][3]
        for r in range(rg,rg+6):
            result_ground += ", h" + str(y+1) + ":" + ground_mas[r][2]
            y+=1
        rg += 6
        y = 0
        result_ground += "},\n"
    result += "{\n air: [\n" + result_air + "],\n ground: [" + result_ground + "]}"
    return result
def break_delete(air_time,ground_time):
    at_del = air_time
    gt = ground_time
    cur.execute("DELETE FROM newair where time = :at_del",{"at_del": at_del})
    conn.commit()
    cur.execute("DELETE FROM newground WHERE time = :gt", {"gt": gt})
    conn.commit()
#создание таблиц air, ground, last_parametr
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
            temperature = 'null'
            humidity = 'null'
            time = var['timeAIR']
            aird = (result,id,temperature,humidity,time)
            cur.execute("INSERT INTO newair VALUES(?, ?, ?, ?, ?);", aird)
            conn.commit()
            aird = ()

        #запись в таблицу ground
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
            humidity = 'null'
            time = var['timeGROUND']
            grd = (result,id,humidity,time)
            cur.execute("INSERT INTO newground VALUES(?, ?, ?, ?);", grd)
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
            cur.execute("SELECT * from newair WHERE time BETWEEN  DATETIME('now','localtime','-30 minutes') and DATETIME('now','localtime') ORDER BY time,id")
            air = cur.fetchall()
            cur.execute("SELECT * from newground WHERE time BETWEEN  DATETIME('now','localtime','-30 minutes') and DATETIME('now','localtime') ORDER BY time,id")
            ground = cur.fetchall()
            final_result = perevod(air, ground)
            cur.close()
        elif n == 'hour':
            cur.execute("SELECT * from newair WHERE time BETWEEN  DATETIME('now','localtime','-1 hour') and DATETIME('now','localtime') ORDER BY time,id")
            air = cur.fetchall()
            cur.execute("SELECT * from newground WHERE time BETWEEN  DATETIME('now','localtime','-1 hour') and DATETIME('now','localtime') ORDER BY time,id")
            ground = cur.fetchall()
            final_result = perevod(air, ground)
            cur.close()
        elif n == '12hours':
            cur.execute("SELECT * from newair WHERE time BETWEEN  DATETIME('now','localtime','-12 hours') and DATETIME('now','localtime') ORDER BY time,id")
            air = cur.fetchall()
            cur.execute("SELECT * from newground WHERE time BETWEEN  DATETIME('now','localtime','-12 hours') and DATETIME('now','localtime') ORDER BY time,id")
            ground = cur.fetchall()
            final_result = perevod(air, ground)
            cur.close()
        elif n == 'day':
            cur.execute("SELECT * from newair WHERE time BETWEEN  DATETIME('now','localtime','-1 day') and DATETIME('now','localtime') ORDER BY time,id")
            air = cur.fetchall()
            cur.execute("SELECT * from newground WHERE time BETWEEN  DATETIME('now','localtime','-1 day') and DATETIME('now','localtime') ORDER BY time,id")
            ground = cur.fetchall()
            final_result = perevod(air, ground)
            cur.close()
        elif n == 'week':
            cur.execute("SELECT * from newair WHERE time BETWEEN  DATETIME('now','localtime','-1 week') and DATETIME('now','localtime') ORDER BY time,id")
            air = cur.fetchall()
            cur.execute("SELECT * from newground WHERE time BETWEEN  DATETIME('now','localtime','-1 week') and DATETIME('now','localtime') ORDER BY time,id")
            ground = cur.fetchall()
            final_result = perevod(air,ground)

        elif n == 'month':
            cur.execute("SELECT * from newair WHERE time BETWEEN  DATETIME('now','localtime','-1 month') and DATETIME('now','localtime') ORDER BY time,id")
            air = cur.fetchall()
            cur.execute("SELECT * from newground WHERE time BETWEEN  DATETIME('now','localtime','-1 month') and DATETIME('now','localtime') ORDER BY time,id")
            ground = cur.fetchall()
            print(air)
            print(ground)
            final_result = perevod(air,ground)


        else:
            return "Неизвестная дата"
        return final_result
    else:
        return "Неверный формат"

print(time_period('month'))
