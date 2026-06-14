import tkinter as tk
from PIL import *

# mouse class (currently only tracks position)
class Mouse:
    def __init__(self):
        self.x = 0
        self.y = 0
    
    def update(self, root):
        self.x = root.winfo_pointerx() - root.winfo_rootx()
        self.y = root.winfo_pointery() - root.winfo_rooty()
mouse = Mouse()

def drawText(root=None, text="", bg="white", fg="black", fstyle="Arial", fsize=14, extra="normal", padx=0, pady=0):
    label = tk.Label(root, text=text, bg=bg, fg=fg, font=(fstyle, fsize, extra), padx=padx, pady=pady)
    label.grid()
    return label

def functionButton(root=None, text="", bg="white", fg="black", fstyle="Arial", fsize=14, extra="normal", padx=0, pady=0, command=None):
    button = tk.Button(root, text=text, bg=bg, fg=fg, font=(fstyle, fsize, extra), padx=padx, pady=pady, command=lambda: command)
    button.grid()
    return button

def linkButton(root=None, text="", bg="white", fg="black", fstyle="Arial", fsize=14, extra="normal", padx=0, pady=0, controller=None, page=None):
    button = tk.Button(root, text=text, bg=bg, fg=fg, font=(fstyle, fsize, extra), padx=padx, pady=pady, command=lambda: controller.show_frame(page))
    button.grid()
    return button