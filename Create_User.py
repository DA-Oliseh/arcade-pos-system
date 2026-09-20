import sqlite3
import bcrypt
connection=sqlite3.connect("arcade.db")
cursor=connection.cursor()
username="Dygovybz"
plain_password="awohlan"
role="Cashier"
password_hash=bcrypt.hashpw(plain_password.encode(),bcrypt.gensalt())
cursor.execute("INSERT INTO users(username,password_hash,role) VALUES(?,?,?)",(username,password_hash,role))
connection.commit()
connection.close()
print("User created successfully!")
