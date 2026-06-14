import tkinter as tk
from PIL import Image, ImageTk
# mouse class (currently only tracks position) NOTE: from old program for now ignore
class Mouse:
    def __init__(self):
        self.x = 0
        self.y = 0
    
    def update(self, stage):
        self.x = stage.winfo_pointerx() - stage.winfo_rootx()
        self.y = stage.winfo_pointery() - stage.winfo_rooty()
mouse = Mouse()

# NOTE: Lazy man code
# commonly used functions and variables are stored here to avoid making main.py messy

def frame(stage=None, bg="#ffffff", column=0, row=0, columnspan=1, rowspan=1, sticky="", columnNum=None, rowNum=None):
    frame = tk.Frame(stage, bg=bg)
    frame.grid(column=column, row=row, columnspan=columnspan, rowspan=rowspan, sticky=sticky)
    if columnNum is not None: #NOTE: use if here bc if you set columnNum to 0 it will skip the for i in range() since range(0) = just skips
        for i in range(columnNum): 
            frame.columnconfigure(i, weight=1)
    else:
        frame.columnconfigure(0, weight=1)
    if rowNum is not None:
        for i in range(rowNum):
            frame.rowconfigure(i, weight=1)
    else:
        frame.rowconfigure(0, weight=1)
    return frame # return frame so you can use it to place other widgets inside it
    # NOTE: eg. headerFrame = frame(yadda yadda)
    # NOTE: con. drawText(stage=headerFrame, yadda yadda) instead of drawText(stage=root, yadda yadda) (changed root to self remember >:[ )


def drawText(stage=None, text="", bg="white", fg="black", fstyle="Arial", fsize=14, extra="normal", padx=0, pady=0, sticky="", column=0, row=0, columnspan=1, rowspan=1):
    label = tk.Label(stage, text=text, bg=bg, fg=fg, font=(fstyle, fsize, extra), padx=padx, pady=pady)
    label.grid(sticky=sticky, column=column, row=row, columnspan=columnspan, rowspan=rowspan)
    return label # return label so you can use it to change the text later (eg. label.config(text="new text")) (for dynamic text like score, timer, etc.)

def functionButton(stage=None, text="", bg="white", fg="black", fstyle="Arial", fsize=14, extra="normal", padx=0, pady=0, sticky="", command=None):
    button = tk.Button(stage, text=text, bg=bg, fg=fg, font=(fstyle, fsize, extra), padx=padx, pady=pady, command=lambda: command)
    button.grid(sticky=sticky)
    return button

def linkButton(stage=None, text="", bg="white", fg="black", fstyle="Arial", fsize=14, extra="normal", padx=0, pady=0, sticky="", controller=None, page=None, column=0, row=0, columnspan=1, rowspan=1):
    button = tk.Button(stage, text=text, bg=bg, fg=fg, font=(fstyle, fsize, extra), padx=padx, pady=pady, command=lambda: controller.show_frame(page))
    button.grid(sticky=sticky, column=column, row=row, columnspan=columnspan, rowspan=rowspan,)
    return button

def drawEntry(stage=None, bg="white", fg="black", fstyle="Arial", fsize=14, extra="normal", padx=0, pady=0, sticky="", column=0, row=0, columnspan=1, rowspan=1):
    entry = tk.Entry(stage, bg=bg, fg=fg, font=(fstyle, fsize, extra))
    entry.grid(sticky=sticky, column=column, row=row, columnspan=columnspan, rowspan=rowspan, padx=padx, pady=pady)
    return entry

def image(stage=None, fileDIR=None, size=[100,100], sticky=""):
        try:
            pil_image = Image.open(fileDIR)
            resized_image = pil_image.resize((size[0], size[1]), Image.Resampling.LANCZOS) # NOTE: .Resampling.LANCZOS allows resizing/changing pixel ratio
            tk_image = ImageTk.PhotoImage(resized_image)
            image_label = tk.Label(stage, image=tk_image)
            image_label.grid(sticky=sticky)
            image_label.image = tk_image
            return image_label
        except:
             print("err: please check file directory and stage")