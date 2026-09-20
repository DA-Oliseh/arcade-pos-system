import sqlite3
import random
from datetime import datetime, timedelta

connection = sqlite3.connect("arcade.db")
cursor = connection.cursor()

cursor.execute("DELETE FROM transactions")
cursor.execute("DELETE FROM sqlite_sequence WHERE name = 'transactions'")

cursor.execute("SELECT item_id, coin_cost FROM arcade")
arcade_items = cursor.fetchall()

cursor.execute("SELECT snack_id, price FROM snacks")
snack_items = cursor.fetchall()

cursor.execute("SELECT station_id, hourly_rate FROM stations")
station_items = cursor.fetchall()

today = datetime.now()

for days_ago in range(7, -1, -1):
    day = today - timedelta(days=days_ago)
    num_transactions = random.randint(8, 20)

    for _ in range(num_transactions):
        hour = random.randint(9, 21)
        minute = random.randint(0, 59)
        timestamp = day.replace(hour=hour, minute=minute, second=0).strftime("%Y-%m-%d %H:%M:%S")

        transaction_kind = random.choice(["game", "game", "snack", "station"])

        if transaction_kind == "game":
            item_id, coin_cost = random.choice(arcade_items)
            cursor.execute(
                "INSERT INTO transactions (transaction_type, item_id, coins_used, transaction_time) VALUES (?, ?, ?, ?)",
                ("game", item_id, coin_cost, timestamp)
            )
        elif transaction_kind == "snack":
            snack_id, price = random.choice(snack_items)
            cursor.execute(
                "INSERT INTO transactions (transaction_type, snack_id, amount_paid, transaction_time) VALUES (?, ?, ?, ?)",
                ("snack", snack_id, price, timestamp)
            )
        else:
            station_id, hourly_rate = random.choice(station_items)
            minutes = random.choice([15, 30, 45, 60, 90])
            amount = round((hourly_rate / 60) * minutes, 2)
            cursor.execute(
                "INSERT INTO transactions (transaction_type, station_id, duration_minutes, amount_paid, transaction_time) VALUES (?, ?, ?, ?, ?)",
                ("station", station_id, minutes, amount, timestamp)
            )

connection.commit()
connection.close()

print("Demo transactions seeded successfully!")