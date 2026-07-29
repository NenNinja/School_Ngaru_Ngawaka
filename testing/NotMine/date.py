import tkinter as tk
from tkcalendar import DateEntry




root = tk.Tk()
root.title("Tkinter Date Entry Example")
root.geometry("350x200")

date_input = DateEntry(
    root,
    width=16,
    background="darkblue",
    foreground="white",
    borderwidth=2,
    date_pattern="yyyy-mm-dd",
)
date_input.pack(pady=10)

root.mainloop()
