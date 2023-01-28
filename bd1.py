import json
import sqlite3
conn = sqlite3.connect('data1.db')
cur = conn.cursor()

#создание таблиц sensor, syslog, types
cur.execute("""CREATE TABLE IF NOT EXISTS sensor(
	 dt	TEXT NOT NULL,
	 id	INTEGER NOT NULL,
	 type INTEGER NOT NULL,
	 value REAL NOT NULL,
	 state INTEGER NOT NULL,
	UNIQUE("dt","id","type")
)
""")
conn.commit()
cur.execute("""CREATE TABLE IF NOT EXISTS syslog(
	 dt TEXT NOT NULL,
	 source INTEGER NOT NULL,
	 message TEXT NOT NULL
)

""")
conn.commit()
cur.execute("""CREATE TABLE IF NOT EXISTS types(
	id INTEGER NOT NULL UNIQUE,
	name TEXT NOT NULL,
	PRIMARY KEY("id")
) WITHOUT ROWID

""")
conn.commit()
