import sqlite3
DB_NAME="arcade.db"
connection=sqlite3.connect(DB_NAME)
cursor=connection.cursor()
cursor.execute("DELETE FROM arcade")
cursor.execute("DELETE FROM snacks")
cursor.execute("DELETE FROM stations")
cursor.execute("DELETE FROM sqlite_sequence WHERE name IN ('arcade','stations','snacks')")
connection.commit()
connection.close()
print("All reference tables cleared!")