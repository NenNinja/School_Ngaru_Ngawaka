import tkinter as tk
import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

def setup_db():
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS data (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                button_name   TEXT    NOT NULL UNIQUE,
                button_text   TEXT    NOT NULL
            )
        """)
    cursor.execute("PRAGMA table_info(data)")
    for i in range(9):
        try:
            cursor.execute("INSERT INTO data (button_name, button_text) VALUES (?, ?)", (f"button{i+1}", f"information{i+1}"))
        except sqlite3.IntegrityError:
            pass
    
setup_db()

class MAIN(tk.Tk):
    def __init__(self, W, H):
        super().__init__()
        self.geometry(f"{W}x{H}")
        self.label = tk.Label(self, text="")
        self.label.grid(row=0, column=4)

    def create_buttons(self):
        index = 0
        for i in cursor.execute("SELECT button_name FROM data").fetchall():
            info = cursor.execute("SELECT button_text FROM data WHERE button_name=?", (i[0],)).fetchone()
            btn = tk.Button(self, text=i, command=lambda info=info: self.label.config(text=info[0]))
            btn.grid(row=int(index/3), column=index-int(index/3)*3)
            index += 1

print(cursor.execute("SELECT * FROM data").fetchall())

main_app = MAIN(400, 400)
main_app.create_buttons()
main_app.mainloop()