import sqlite3
from pathlib import Path

scriptDIR = Path(__file__).resolve().parent
conn = sqlite3.connect(scriptDIR / "userInformation.db")
cursor = conn.cursor()

def insert(field, value):
    cursor.execute(f"INSERT INTO users ({field}) VALUES (?)", (value,))
    conn.commit()

def select(field):
    cursor.execute(f"SELECT {field} FROM users")
    return cursor.fetchall()

list = select("*")
for i in list:
    print(i)

conn.close()