import json
import sqlite3
conn = sqlite3.connect('data.db')
cur = conn.cursor()

#создание таблиц time, air, ground
cur.execute("""CREATE TABLE IF NOT EXISTS time(
   time TEXT,
   type TEXT);
""")
conn.commit()
cur.execute("""CREATE TABLE IF NOT EXISTS air(
   type TEXT,
   result TEXT,
   id TEXT,
   temperature TEXT,
   humidity TEXT,
   time TEXT);
""")
conn.commit()
cur.execute("""CREATE TABLE IF NOT EXISTS ground(
   type TEXT,
   result TEXT,
   id TEXT,  
   humidity TEXT,
   time TEXT);
""")
conn.commit()

#работа с кортежами для занесения данных в таблицу
var = {'timeAIR': '2023-01-22 13:24:07',
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
#запись в таблицу air

for i in range(0,4):
    if (str(var['data']['air'][i]['result']) == 'True'):
        type = '1'
        result = str(var['data']['air'][i]['result'])
        id = str(var['data']['air'][i]['id'])
        temperature = str(var['data']['air'][i]['temperature'])
        humidity = str(var['data']['air'][i]['humidity'])
        time = '-'
        aird = (type,result,id,temperature,humidity,time)
        cur.execute("INSERT INTO air VALUES(?, ?, ?, ?, ?, ?);", aird)
        conn.commit()
        aird = ()
    else:
        type = '1'
        result = str(var['data']['air'][i]['result'])
        id = str(var['data']['air'][i]['id'])
        temperature = 'NULL'
        humidity = 'NULL'
        time = '-'
        aird = (type,result,id,temperature,humidity,time)
        cur.execute("INSERT INTO air VALUES(?, ?, ?, ?, ?, ?);", aird)
        conn.commit()
        aird = ()

#запись в таблицу ground
for i in range(0,6):
    if (str(var['data']['ground'][i]['result']) == 'True'):
        type = '1'
        result = str(var['data']['ground'][i]['result'])
        id = str(var['data']['ground'][i]['id'])
        humidity = str(var['data']['ground'][i]['humidity'])
        time = '-'
        grd = (type,result,id,humidity,time)
        cur.execute("INSERT INTO ground VALUES(?, ?, ?, ?, ?);", grd)
        conn.commit()
        grd = ()
    else:
        type = '1'
        result = str(var['data']['ground'][i]['result'])
        id = str(var['data']['ground'][i]['id'])
        humidity = 'NULL'
        time = '-'
        grd = (type,result,id,humidity,time)
        cur.execute("INSERT INTO ground VALUES(?, ?, ?, ?, ?);", grd)
        conn.commit()
        grd = ()


cur.execute("SELECT * FROM air;")
all_results = cur.fetchall()
print(all_results)
cur.execute("SELECT * FROM ground;")
all_results1 = cur.fetchall()
print(all_results1)
conn.close()



