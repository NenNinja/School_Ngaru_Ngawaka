import sqlite3

conn = sqlite3.connect("testing.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id      INTEGER     PRIMARY     KEY     AUTOINCREMENT,
        name    TEXT        NOT NULL
    )
""")

def insert(field, value):
    cursor.execute(f"INSERT INTO users ({field}) VALUES (?)", (value,))
    conn.commit()

def select(field):
    cursor.execute(f"SELECT {field} FROM users")
    return cursor.fetchall()

a = True

while a:
    list = select(input("enter field to select (id/name/ *): "))    
    for i in list:
        print(i)



conn.commit()
conn.close()
