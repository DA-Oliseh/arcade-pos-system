import sqlite3
import streamlit as st
import bcrypt
import pandas as pd
from database import create_tables
create_tables()
st.set_page_config(page_title="Arcade POS System",layout="wide")
#First time set-up check
connection=sqlite3.connect("arcade.db")
cursor=connection.cursor()
cursor.execute("SELECT COUNT(*) FROM users")
user_count=cursor.fetchone()[0]
connection.close()
if user_count==0:
    st.header("First-time set up:Create Admin account")
    col1,col2,col3=st.columns([1,2,1])
    with col2:
      new_user=st.text_input("Enter a username")
      new_password=st.text_input("Enter password",type="password")
      if st.button("Create Admin account"):
        password_hash=bcrypt.hashpw(new_password.encode(),bcrypt.gensalt())
        connection=sqlite3.connect("arcade.db")
        cursor=connection.cursor()
        cursor.execute("INSERT INTO users(username,password_hash,role) VALUES(?,?,?)",(new_user,password_hash,"admin"))
        connection.commit()
        connection.close()
        st.success("Admin account created!Please refresh and log in.")
        st.stop()
    st.stop()
if "logged_in" not in st.session_state:
    st.session_state.logged_in=False
if not st.session_state.logged_in:
    st.header("Login")
    col1,col2,col3=st.columns([1,2,3])
    with col2:
     username_input=st.text_input("Username")
     password_input=st.text_input("Password",type="password")
     if st.button("Login"):
        connection=sqlite3.connect("arcade.db")
        cursor=connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?",(username_input,))
        user=cursor.fetchone()
        connection.close()
        if user and bcrypt.checkpw(password_input.encode(),user[2]):
            st.session_state.logged_in=True
            st.session_state.username=user[1]
            st.session_state.role=user[3]
            st.rerun()

        else:
            st.error("Incorrect username or password")
    st.stop()
if st.session_state.logged_in:
    st.sidebar.write(f"Logged in as: {st.session_state.username} {st.session_state.role}")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in=False
        st.rerun()
st.title("Arcade POS System")
if st.session_state.role=="admin":
    tab_names=["Arcade Games","Consoles","Racing","Snacks","Reports","Coin Inventory","Manage Users"]
else:
    tab_names=["Arcade Games","Consoles","Racing","Snacks","Reports"]
tabs=st.tabs(tab_names)
tab1=tabs[0]
tab2=tabs[1]
tab3=tabs[2]
tab4=tabs[3]
tab5=tabs[4]
if st.session_state.role=="admin":
    tab6=tabs[5]
    tab7=tabs[6]
with tab1:
    st.header("Arcade Games")
    connection=sqlite3.connect("arcade.db")
    cursor=connection.cursor()
    cursor.execute("SELECT * FROM arcade")
    games=cursor.fetchall()
    connection.close()
    items_per_row=3
    for row_start in range(0,len(games),items_per_row):
        row_games=games[row_start:row_start + items_per_row]
        columns=st.columns(items_per_row)
        for col,game in zip(columns,row_games):
            with col:
              st.write(f"{game[1]} - {game[2 ]} coins")
              if st.button(f"Log sale: {game[1]}", type="primary"):
                    connection = sqlite3.connect("arcade.db")
                    cursor = connection.cursor()
                    cursor.execute(
                        "INSERT INTO transactions (transaction_type, item_id, coins_used, transaction_time) VALUES (?, ?, ?, datetime('now'))",
                        ("game", game[0], game[2])
                    )
                    connection.commit()
                    connection.close()
                    st.success(f"Sale logged: {game[1]}")
with tab2:
    st.header("Consoles")
    connection = sqlite3.connect("arcade.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM stations WHERE type = ?", ("console",))
    consoles = cursor.fetchall()
    connection.close()

    items_per_row = 3

    for row_start in range(0, len(consoles), items_per_row):
        row_stations = consoles[row_start:row_start + items_per_row]
        columns = st.columns(items_per_row)

        for col, station in zip(columns, row_stations):
            with col:
                st.write(f"{station[1]} — Ksh {station[3]} per hour")
                minutes = st.number_input(f"Minutes for {station[1]}", min_value=1, max_value=180, value=60, key=f"minutes_{station[0]}")

                if st.button(f"Log sale: {station[1]}", key=f"logsale_console_{station[0]}", type="primary"):
                    amount = round((station[3] / 60) * minutes, 2)
                    connection = sqlite3.connect("arcade.db")
                    cursor = connection.cursor()
                    cursor.execute(
                        "INSERT INTO transactions (transaction_type, station_id, duration_minutes, amount_paid, transaction_time) VALUES (?, ?, ?, ?, datetime('now'))",
                        ("station", station[0], minutes, amount)
                    )
                    connection.commit()
                    connection.close()
                    st.success(f"Sale logged: {station[1]} for {minutes} minutes — Ksh {amount:.2f}")
with tab3:
    st.header("Racing")
    connection = sqlite3.connect("arcade.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM stations WHERE type = ?", ("racing",))
    racing_stations = cursor.fetchall()
    connection.close()

    items_per_row = 3

    for row_start in range(0, len(racing_stations), items_per_row):
        row_stations = racing_stations[row_start:row_start + items_per_row]
        columns = st.columns(items_per_row)

        for col, station in zip(columns, row_stations):
            with col:
                st.write(f"{station[1]} — Ksh {station[3]} per hour")
                minutes = st.number_input(f"Minutes for {station[1]}", min_value=1, max_value=180, value=60, key=f"minutes_{station[0]}")

                if st.button(f"Log sale: {station[1]}", key=f"logsale_racing_{station[0]}", type="primary"):
                    amount = round((station[3] / 60) * minutes, 2)
                    connection = sqlite3.connect("arcade.db")
                    cursor = connection.cursor()
                    cursor.execute(
                        "INSERT INTO transactions (transaction_type, station_id, duration_minutes, amount_paid, transaction_time) VALUES (?, ?, ?, ?, datetime('now'))",
                        ("station", station[0], minutes, amount)
                    )
                    connection.commit()
                    connection.close()
                    st.success(f"Sale logged: {station[1]} for {minutes} minutes — Ksh {amount:.2f}")
    
with tab4:
    st.header("Snacks")
    connection = sqlite3.connect("arcade.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM snacks")
    snacks = cursor.fetchall()
    connection.close()

    items_per_row = 3

    for row_start in range(0, len(snacks), items_per_row):
        row_snacks = snacks[row_start:row_start + items_per_row]
        columns = st.columns(items_per_row)

        for col, snack in zip(columns, row_snacks):
            with col:
                st.write(f"{snack[1]} — Ksh {snack[2]}")
                if st.button(f"Log sale: {snack[1]}", key=f"logsale_snack_{snack[0]}", type="primary"):
                    connection = sqlite3.connect("arcade.db")
                    cursor = connection.cursor()
                    cursor.execute(
                        "INSERT INTO transactions (transaction_type, snack_id, amount_paid, transaction_time) VALUES (?, ?, ?, datetime('now'))",
                        ("snack", snack[0], snack[2])
                    )
                    connection.commit()
                    connection.close()
                    st.success(f"Sale logged: {snack[1]} — Ksh {snack[2]}")
with tab5:
    st.header("Reports")
    start_date=st.date_input("Start date")
    end_date=st.date_input("End date")
    if st.button("Generate Report"):
        connection=sqlite3.connect("arcade.db")
        cursor=connection.cursor()
        cursor.execute("SELECT * FROM transactions WHERE date(transaction_time) BETWEEN ? AND ?",(str(start_date),str(end_date)))
        results=cursor.fetchall()
        cursor.execute("SELECT transaction_type,SUM(amount_paid),SUM(coins_used), COUNT(*) FROM transactions WHERE date(transaction_time) BETWEEN ? AND ? GROUP BY transaction_type",(str(start_date),str(end_date)))
        breakdown=cursor.fetchall()
        connection.close()
        st.write(f"Found {len(results)} transactions")
        st.subheader("Breakdown by type")
        for row in breakdown:
            type_name,cash,coins,count=row
            st.write(f"**{type_name}** - {count} transactions, KSh {cash or 0:.2f}, {coins or 0} coins used")
        st.subheader("All transactions")
        for row in results:
         st.write(row)
        cursor_conn=sqlite3.connect("arcade.db")
        chart_data=pd.read_sql_query("SELECT date(transaction_time) as day, SUM(amount_paid) as revenue FROM transactions WHERE date(transaction_time) BETWEEN ? AND ? GROUP BY day ORDER BY day",cursor_conn,params=(str(start_date),str(end_date)))
        cursor_conn.close()
        st.subheader("Revenue over time")
        if not chart_data.empty:
            chart_data=chart_data.set_index("day")
            st.line_chart(chart_data)
        else:
            st.write("No revenue data for this period")

if st.session_state.role=="admin":
    with tab6:
     st.header("Coin Inventory")
     connection=sqlite3.connect("arcade.db")
     cursor=connection.cursor()
     cursor.execute("SELECT * FROM coin_inventory ORDER BY updated_at DESC LIMIT 1")
     latest=cursor.fetchone()
     connection.close()
     if latest:
        last_restock=latest[1]
        last_restock_time=latest[3]
     else:
        last_restock=0
        last_restock_time= "Never"
     connection=sqlite3.connect("arcade.db")
     cursor=connection.cursor()
     cursor.execute("SELECT SUM(coins_used) FROM transactions WHERE transaction_time>?",(last_restock_time if latest else "2000-01-01",))
     used_since=cursor.fetchone()[0] or 0
     connection.close()
     remaining=last_restock - used_since
     if latest:
       st.write(f"Last restock: {last_restock} coins, at {last_restock_time}")
       st.write(f"Coins used since: {used_since}")
       st.write(f"**Coins remaining: {remaining}**")
     else:
        st.warning("No restock recorded yet -Please enter your current coin count below to get started")
     new_total=st.number_input("New coin count (admin restock)",min_value=0,value=0)
     if st.button("Restock"):
        connection=sqlite3.connect("arcade.db")
        cursor=connection.cursor()
        cursor.execute("INSERT INTO coin_inventory(total_coins,updated_by,updated_at) VALUES(?,?,datetime('now'))",(new_total,"admin"))
        connection.commit()
        connection.close()
        st.success(f"Restocked to {new_total} coins")
    with tab7:
        st.header("Manage Users")
        connection=sqlite3.connect("arcade.db")
        cursor=connection.cursor()
        cursor.execute("SELECT username,role FROM users")
        existing_users=cursor.fetchall()
        connection.close()
        st.subheader("Existing users")
        for user_row in existing_users:
            st.write(f"{user_row[0]} - {user_row[1]}")
        st.subheader("Create new user")
        new_username=st.text_input("New username",key="Manage_new_username")
        new_password=st.text_input("New password",type="password",key="manage_new_password")
        new_role=st.selectbox("Role",["cashier","admin"])
        if st.button("Create user"):
            password_hash=bcrypt.hashpw(new_password.encode(),bcrypt.gensalt())
            connection=sqlite3.connect("arcade.db")
            cursor=connection.cursor()
            try:
                cursor.execute("INSERT INTO users (username,password_hash,role) VALUES(?,?,?)",(new_username,password_hash,new_role))
                connection.commit()
            except sqlite3.IntegrityError:
                st.error("That username already exists - Please choose another.")
            connection.close()