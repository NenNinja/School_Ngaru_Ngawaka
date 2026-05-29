import tkinter as tk

# main init function (sets dimensions and title while also returning the root object for use in other functions)
def init_app(x, y, title="unnamed"):
    global root #IMPORTAMT! global to allow use in other functions in library without needing to pass root as an argument
    root = tk.Tk()
    root.title(title)
    root.geometry(f"{x}x{y}")
    return root

# mouse class (currently only tracks position)
class Mouse:
    def __init__(self):
        self.x = 0
        self.y = 0
    
    def update(self):
        self.x = root.winfo_pointerx() - root.winfo_rootx()
        self.y = root.winfo_pointery() - root.winfo_rooty()
mouse = Mouse()

def drawText(root=None, string="", color = "black", pos=[0, 0], size=12):
    label = tk.Label(root, text=string, font=("Arial", size), fg=color)
    label.place(x=pos[0], y=pos[1])
    return label

def drawButton(root=None, string="", pos=[0, 0], command=None):
    button = tk.Button(root, text=string, command=command)
    button.place(x=pos[0], y=pos[1])
    return button