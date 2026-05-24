import tkinter as tk

def init_app():
    global root
    root = tk.Tk()
    root.title("Simple App")
    root.geometry("300x200")
    
def get_mouse_position():
    global mouse_position
    mouse_position = (root.winfo_pointerx() - root.winfo_rootx(), 
                      root.winfo_pointery() - root.winfo_rooty())

def update():
    get_mouse_position()
    text2.config(text=f"Mouse Position: ({mouse_position[0]}, {mouse_position[1]})")

    root.after(10, update)

def setup():
    text1 = tk.Label(root, text="Hello, Tkinter!")
    text1.pack()
    button = tk.Button(root, text="Click Me", command=lambda: text1.config(text="Button Clicked!"))
    button.pack()

    global text2
    text2 = tk.Label(root, text=f"Mouse Position: (0,0)")
    text2.pack()


init_app()
setup()
update()
root.mainloop()
