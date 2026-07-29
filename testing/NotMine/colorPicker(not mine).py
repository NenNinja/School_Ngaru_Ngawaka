import tkinter as tk
from tkinter import colorchooser

def pick_color():
    color_code = colorchooser.askcolor(title="Choose a color")
    if color_code[1]: # Check if a color was selected (not canceled)
        root.config(bg=color_code[1]) # Change window background

root = tk.Tk()
root.geometry("300x200")

button = tk.Button(root, text="Select Color", command=pick_color)
button.pack(pady=50)

root.mainloop()
