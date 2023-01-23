import json
import sqlite3
conn = sqlite3.connect('data.db')
cur = conn.cursor()

#создание таблиц air, ground
cur.execute("""CREATE TABLE IF NOT EXISTS newair(
   result TEXT,
   id TEXT,
   temperature TEXT,
   humidity TEXT,
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
        result = str(var['data']['air'][i]['result'])
        id = str(var['data']['air'][i]['id'])
        temperature = str(var['data']['air'][i]['temperature'])
        humidity = str(var['data']['air'][i]['humidity'])
        time = var['timeAIR']
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
        humidity = 'NULL'
        time = var['timeAIR']
        grd = (result,id,humidity,time)
        cur.execute("INSERT INTO newground VALUES(?, ?, ?, ?);", grd)
        conn.commit()
        grd = ()

#вывод

cur.execute("SELECT * FROM newair ORDER BY time;")
all_results = cur.fetchall()
print(all_results)
cur.execute("SELECT * FROM newground ORDER BY time;")
all_results1 = cur.fetchall()
print(all_results1)
conn.close()

#вывод данных за определённый промежуток(минута, 10 минут, полчаса, час, 12 часов, день)
