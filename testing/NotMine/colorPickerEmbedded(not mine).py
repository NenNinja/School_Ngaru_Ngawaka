import tkinter as tk
from tkinter import ttk

class EmbeddedColorPicker(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Color values (0 to 255)
        self.r_var = tk.IntVar(value=128)
        self.g_var = tk.IntVar(value=128)
        self.b_var = tk.IntVar(value=255)
        
        self.create_widgets()
        self.update_color()

    def create_widgets(self):
        # Preview block for the selected color
        self.preview = tk.Frame(self, width=150, height=150, relief="ridge", bd=2)
        self.preview.pack(side=tk.LEFT, padx=20, pady=20)
        self.preview.pack_propagate(False)
        
        # Label to display the hex string
        self.hex_label = tk.Label(self.preview, text="", font=("Courier", 11, "bold"))
        self.hex_label.pack(expand=True)

        # Control panel for sliders
        slider_frame = tk.Frame(self)
        slider_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Build individual slider setups
        self.build_slider(slider_frame, "Red:", self.r_var, "red")
        self.build_slider(slider_frame, "Green:", self.g_var, "green")
        self.build_slider(slider_frame, "Blue:", self.b_var, "blue")

    def build_slider(self, parent, label_text, variable, accent_color):
        row_frame = tk.Frame(parent)
        row_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(row_frame, text=label_text, width=6, anchor="w").pack(side=tk.LEFT)
        
        # The slider calls self.update_color on movement
        slider = ttk.Scale(row_frame, from_=0, to=255, variable=variable, command=lambda _: self.update_color())
        slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Value readout label
        val_label = tk.Label(row_frame, text="", width=4)
        val_label.pack(side=tk.RIGHT)
        
        # Keep track of label references to update them dynamically
        if not hasattr(self, 'value_labels'):
            self.value_labels = {}
        self.value_labels[str(variable)] = val_label

    def update_color(self):
        r, g, b = self.r_var.get(), self.g_var.get(), self.b_var.get()
        
        # Convert RGB to Hex
        hex_code = f"#{r:02x}{g:02x}{b:02x}"
        
        # Update preview frame background and text
        self.preview.config(bg=hex_code)
        self.hex_label.config(text=hex_code, bg=hex_code, fg="#ffffff" if (r+g+b)<380 else "#000000")
        
        # Update numeric readouts
        self.value_labels[str(self.r_var)].config(text=str(r))
        self.value_labels[str(self.g_var)].config(text=str(g))
        self.value_labels[str(self.b_var)].config(text=str(b))

# Main Execution Loop
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Embedded Color Picker Example")
    root.geometry("450x200")
    
    picker = EmbeddedColorPicker(root)
    picker.pack(fill=tk.BOTH, expand=True)
    
    root.mainloop()
