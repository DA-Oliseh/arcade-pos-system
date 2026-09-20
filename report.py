"""
import sqlite3
connection=sqlite3.connect("arcade.db")
cursor=connection.cursor()
start_date="2026-08-31"
end_date="2026-09-06"
cursor.execute("SELECT * FROM transactions WHERE date(transaction_time) BETWEEN ? AND ?",(start_date,end_date))
results=cursor.fetchall()
for row in results:
    print(row)
connection.close()
"""
import sqlite3
connection=sqlite3.connect("arcade.db")
cursor=connection.cursor()
cursor.execute("SELECT * FROM transactions")
results=cursor.fetchall()
for row in results:
    print(row)
connection.close()