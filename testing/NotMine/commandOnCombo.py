import tkinter as tk
from tkinter import ttk

# 1. Define the callback function (it must accept an 'event' argument)
def on_item_selected(event):
    # Retrieve the selected item directly from the widget that triggered the event
    selected_value = event.widget.get()
    print(f"You selected: {selected_value}")

# Set up the main window
root = tk.Tk()
root.title("Combobox Event Trigger")
root.geometry("300x150")

# Create a list of options
options = ["Option 1", "Option 2", "Option 3"]

# Create the Combobox widget
combo = ttk.Combobox(root, values=options, state="readonly")
combo.pack(pady=40)

# 2. Bind the virtual event to the callback function
combo.bind("<<ComboboxSelected>>", on_item_selected)

root.mainloop()
