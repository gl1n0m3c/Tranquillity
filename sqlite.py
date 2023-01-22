import json
import sqlite3
conn = sqlite3.connect('data.db')
cur = conn.cursor()

#создание таблиц time, air, ground
cur.execute("""CREATE TABLE IF NOT EXISTS time(
   time TEXT,
   type INT);
""")
conn.commit()
cur.execute("""CREATE TABLE IF NOT EXISTS air(
   type INT,
   result INT,
   id INT,
   temperature REAL,
   humidity REAL,
   time TEXT);
""")
conn.commit()
cur.execute("""CREATE TABLE IF NOT EXISTS ground(
   type INT,
   result INT,
   id INT,  
   humidity REAL,
   time TEXT);
""")
conn.commit()

#работа с кортежами для занесения данных в таблицу
var = {'timeAIR': '2023-01-22 13:04:10',
       'timeGROUND': '2023-01-22 13:04:10',
       'data': {
           'air': [{'result': True, 'id': 1, 'temperature': 28.35, 'humidity': 74.54},
                   {'result': True, 'id': 2, 'temperature': 31.96, 'humidity': 64.07},
                   {'result': True, 'id': 3, 'temperature': 28.92, 'humidity': 73.09},
                   {'result': True, 'id': 4, 'temperature': 29.49, 'humidity': 62.76}],
           'ground': [{'result': True, 'id': 1, 'humidity': 70.81},
                      {'result': True, 'id': 2, 'humidity': 68.25},
                      {'result': True, 'id': 3, 'humidity': 65.44},
                      {'result': True, 'id': 4, 'humidity': 75.3},
                      {'result': True, 'id': 5, 'humidity': 72.79},
                      {'result': True, 'id': 6, 'humidity': 70.41}]}}
