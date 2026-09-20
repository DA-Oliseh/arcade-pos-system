import sqlite3
DB_NAME= "arcade.db"
def create_tables():
    connection=sqlite3.connect(DB_NAME)
    cursor=connection.cursor()
    cursor.execute("""
           CREATE TABLE IF NOT EXISTS arcade(
           item_id INTEGER PRIMARY KEY AUTOINCREMENT,
           name TEXT NOT NULL,
           coin_cost INTEGER NOT NULL
           )
           """)
    cursor.execute("""
           CREATE TABLE IF NOT EXISTS snacks(
           snack_id INTEGER PRIMARY KEY AUTOINCREMENT,
           name TEXT NOT NULL,
           price REAL NOT NULL
           )
           """)
    cursor.execute("""
           CREATE TABLE IF NOT EXISTs stations(
           station_id INTEGER PRIMARY KEY AUTOINCREMENT,
           name TEXT NOT NULL,
           type TEXT NOT NULL,
           hourly_rate REAL NOT NULL,
           ip_address TEXT NOT NULL)
           """)
    cursor.execute("""
           CREATE TABLE IF NOT EXISTS transactions(
           transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
           transaction_type TEXT NOT NULL,
           item_id INTEGER,
           snack_id INTEGER,
           station_id INTEGER,
           players INTEGER DEFAULT 1,
           duration_minutes INTEGER,
           coins_used INTEGER,
           amount_paid REAL,
           cashier_name TEXT,
           transaction_time TEXT NOT NULL)
           """)
    cursor.execute("""CREATE TABLE IF NOT EXISTS  coin_inventory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    total_coins INTEGER NOT NULL,
    updated_by TEXT,
    updated_at TEXT NOT NULL)
    """)
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL)
    """)    
    connection.commit()
    connection.close()
if __name__=="__main__":
    create_tables()
    print("tables created succesfully!")   