import tkinter as tk
from tkinter import ttk

def on_toggle():
    print(f"Checkbox toggled! Current state: {is_checked.get()}") # NOTE: .get() returns tk.BooleanVar()
 
root = tk.Tk()
root.title("Checkbox Example")
root.geometry("300x150")

# 1. Create a variable to hold the checkbox state
is_checked = tk.BooleanVar()

# 2. Create the checkbox
# Pass the function 'on_toggle' to command (no parentheses)
# This delays execution until the user clicks
chk = ttk.Checkbutton(
    root, 
    text="Click me", 
    variable=is_checked, 
    command=on_toggle
)
chk.pack(pady=40)

root.mainloop()
