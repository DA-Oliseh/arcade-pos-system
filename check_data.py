import sqlite3
DB_NAME="arcade.db"
connection=sqlite3.connect(DB_NAME)
cursor=connection.cursor()
#cursor.execute("DELETE FROM arcade")
#cursor.execute("DELETE FROM sqlite_sequence WHERE name='arcede'")
#connection.commit()
print("---Arcade---")
cursor.execute("SELECT * FROM arcade")
for row in cursor.fetchall():
    print(row)
print("---Snacks---")
cursor.execute("SELECT *FROM snacks")
for row in cursor.fetchall():
    print(row)
print("---Stations---")
cursor.execute("SELECT *FROM stations")
for row in cursor.fetchall():
    print(row)
connection.close()
