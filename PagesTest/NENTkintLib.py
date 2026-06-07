import tkinter as tk

# mouse class (currently only tracks position)
class Mouse:
    def __init__(self):
        self.x = 0
        self.y = 0
    
    def update(self, root):
        self.x = root.winfo_pointerx() - root.winfo_rootx()
        self.y = root.winfo_pointery() - root.winfo_rooty()
mouse = Mouse()

def drawText(root=None, text="", bg="white", fg="black", fstyle="Arial", fsize=14, extra="normal", padx=0, pady=0, expand=True, fill=tk.BOTH):
    label = tk.Label(root, text=text, bg=bg, fg=fg, font=(fstyle, fsize, extra), padx=padx, pady=pady)
    label.pack(expand=expand, fill=fill)
    return label

def functionButton(root=None, text="", bg="white", fg="black", fstyle="Arial", fsize=14, extra="normal", padx=0, pady=0, expand=True, fill=tk.BOTH, side=tk.LEFT, command=None):
    button = tk.Button(root, text=text, bg=bg, fg=fg, font=(fstyle, fsize, extra), padx=padx, pady=pady, command=lambda: command)
    button.pack(expand=expand, fill=fill, side=side)
    return button

def linkButton(root=None, text="", bg="white", fg="black", fstyle="Arial", fsize=14, extra="normal", padx=0, pady=0, controller=None, page=None, expand=True, fill=tk.BOTH, side=tk.LEFT):
    button = tk.Button(root, text=text, bg=bg, fg=fg, font=(fstyle, fsize, extra), padx=padx, pady=pady, command=lambda: controller.show_frame(page))
    button.pack(expand=expand, fill=fill, side=side)
    return button