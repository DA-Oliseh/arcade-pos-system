import sqlite3
connection=sqlite3.connect('arcade.db')
cursor=connection.cursor()
cursor.execute("SELECT username,role FROM users")
for row in cursor.fetchall():
    print(row)
connection.close()
