import tkinter as tk

def update_label():
    # 1. Get the new data
    x = root.winfo_pointerx() - root.winfo_rootx()
    y = root.winfo_pointery() - root.winfo_rooty()
    
    # 2. Update the label text
    label2.config(text=f"Mouse Position: ({x}, {y})")
    
    # 3. Schedule the NEXT update (10ms from now)
    # This creates the "constant" loop
    root.after(10, update_label)

root = tk.Tk()
root.geometry("300x200")

label2 = tk.Label(root, text="Mouse Position: (0, 0)", font=("Arial", 14))
label2.pack(pady=50) #pady = vert padding

update_label()

root.mainloop()
