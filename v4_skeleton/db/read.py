import sqlite3
from pathlib import Path

scriptDIR = Path(__file__).resolve().parent
conn = sqlite3.connect(scriptDIR / "userInformation.db")
cursor = conn.cursor()

def select(field):
    cursor.execute(f"SELECT {field} FROM posts")
    return cursor.fetchall()
cursor.execute("SELECT name FROM pragma_table_info('posts')")
print(cursor.fetchall())

list = select("*")
for i in list:
    print(i)
conn.close()