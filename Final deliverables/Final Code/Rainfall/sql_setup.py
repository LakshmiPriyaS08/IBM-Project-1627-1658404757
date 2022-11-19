import sqlite3

conn = sqlite3.connect('user_login.db')
print("Opened database successfully")

conn.execute('CREATE TABLE user (name TEXT, password TEXT, email TEXT)')
print("Table created successfully")
conn.close()