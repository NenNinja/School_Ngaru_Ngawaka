from NENTkintLib import *

def setup():
    root.configure(bg="#FFFFFF")
    
    drawText(root, "Hello, Tkinter!", color="blue", pos=[10, 0], size=16)

    drawButton(root, string="Click Me", pos=[10, 50], command=lambda: drawText(root, "Button Clicked!", pos=[100, 50]))

    drawText(root, "Move the mouse around to see its position.", pos=[10, 100])
    drawText(root, "This is a simple Tkinter app.", pos=[10, 150])

    global text2
    text2 = drawText(root, "Mouse Position: (0,0)", pos=[10, 250])

def update():
    mouse.update()
    text2.config(text=f"Mouse Position: ({mouse.x}, {mouse.y})")

    root.after(10, update)

def main():
    global root
    root = init_app(400, 400, "My Tkinter App")
    setup()
    update()
    root.mainloop()

main()