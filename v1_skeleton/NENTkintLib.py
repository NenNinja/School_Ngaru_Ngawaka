from logging import root
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import colorchooser as colPicker

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

def frame(stage=None, bg="#ffffff", column=0, row=0, columnspan=1, rowspan=1, sticky="", columnNum=0, rowNum=0, showGrid=False, highLightColor="black", highLightWidth=0):
    frame1 = tk.Frame(
        stage, 
        bg=bg, 
        highlightbackground=highLightColor, 
        highlightthickness=highLightWidth 
        )
    frame1.grid(
        column=column, 
        row=row, 
        columnspan=columnspan, 
        rowspan=rowspan, 
        sticky=sticky
        )
    if columnNum != 0: #NOTE: use if here bc if you set columnNum to 0 it will skip the for i in range() since range(0) = just skips
        for i in range(columnNum): 
            frame1.columnconfigure(i, weight=1)
    else:
        frame1.columnconfigure(0, weight=1)
    if rowNum != 0:
        for i in range(rowNum):
            frame1.rowconfigure(i, weight=1)
    else:
        frame1.rowconfigure(0, weight=1)
    frame1.grid_propagate(False)
    
    if showGrid == True: # This grid is for debugging purposes, idea credit goes to Jaco (he inspired the idea for the grid)
        for ix in range(columnNum) if columnNum != 0 else range(1):
            for iy in range(rowNum) if rowNum != 0 else range(1):
                frame(
                    stage=frame1,
                    column=ix, row=iy, 
                    sticky="nsew", 
                    bg="#ffffff",
                    highLightColor="black",   # This sets the border color
                    highLightWidth=1,        # This sets the border width in pixels
                    )
                
    return frame1 # return frame so you can use it to place other widgets inside it
    # NOTE: eg. headerFrame = frame(yadda yadda)
    # NOTE: con. drawText(stage=headerFrame, yadda yadda) instead of drawText(stage=root, yadda yadda) (changed root to self remember >:[ )


def drawText(stage=None, text="", bg="white", fg="black", fstyle="Arial", fsize=14, extra="normal", padx=0, pady=0, sticky="", column=0, row=0, columnspan=1, rowspan=1):
    label = tk.Label(
        stage, 
        text=text, 
        bg=bg, 
        fg=fg, 
        font=(fstyle, fsize, extra), 
        padx=padx, pady=pady
        ).grid(
            sticky=sticky, 
            column=column, row=row, 
            columnspan=columnspan, rowspan=rowspan
            )
    return label # return label so you can use it to change the text later (eg. label.config(text="new text")) (for dynamic text like score, timer, etc.)

def functionButton(stage=None, text="", bg="white", fg="black", fstyle="Arial", fsize=14, extra="normal", padx=0, pady=0, sticky="", command=None, column=0, row=0, columnspan=1, rowspan=1):
    button = tk.Button(
        stage, 
        text=text, 
        bg=bg, 
        fg=fg, 
        font=(fstyle, fsize, extra), 
        padx=padx, pady=pady, 
        command=lambda: command
        ).grid(
            sticky=sticky, 
            column=column, row=row, 
            columnspan=columnspan, rowspan=rowspan
            )
    return button

def linkButton(stage=None, text="", bg="white", fg="black", fstyle="Arial", fsize=14, extra="normal", padx=0, pady=0, sticky="", controller=None, page=None, column=0, row=0, columnspan=1, rowspan=1):
    button = tk.Button(
        stage, 
        text=text, 
        bg=bg, 
        fg=fg, 
        font=(fstyle, fsize, extra), 
        padx=padx, pady=pady, 
        command=lambda: controller.show_frame(page)
        ).grid(
            sticky=sticky, 
            column=column, 
            row=row, 
            columnspan=columnspan, 
            rowspan=rowspan
            )
    return button

def drawEntry(stage=None, bg="white", fg="black", fstyle="Arial", fsize=14, extra="normal", padx=0, pady=0, sticky="", column=0, row=0, columnspan=1, rowspan=1):
    entry = tk.Entry(
        stage, 
        bg=bg, 
        fg=fg, 
        font=(fstyle, fsize, extra)
        ).grid(
            sticky=sticky, 
            column=column, 
            row=row, 
            columnspan=columnspan, 
            rowspan=rowspan, 
            padx=padx, 
            pady=pady
            )
    return entry

def radioButton(stage=None, text="", variable=None, value=None, bg="white", fg="black", fstyle="Arial", fsize=14, extra="normal", padx=0, pady=0, sticky="", column=0, row=0, columnspan=1, rowspan=1):
    radio = ttk.Radiobutton(
        stage, 
        text=text, 
        variable=variable, 
        value=value
        ).grid(
            sticky=sticky, 
            column=column, 
            row=row, 
            columnspan=columnspan, 
            rowspan=rowspan, 
            padx=padx, pady=pady
            )
    return radio

def image(stage=None, fileDIR=None, size=[100,100], sticky="", column=0, row=0, columnspan=1, rowspan=1):
        try:
            resizedImage = Image.open(fileDIR).resize((size[0], size[1]), Image.Resampling.LANCZOS) # NOTE: .Resampling.LANCZOS allows resizing/changing pixel ratio
            tkImage = ImageTk.PhotoImage(resizedImage)
            imageLabel = tk.Label(stage, image=tkImage).grid(sticky=sticky, column=column, row=row, columnspan=columnspan, rowspan=rowspan)
            imageLabel.image = tkImage
            return imageLabel
        except:
             print("err: please check file directory and stage")

def imageCommandButton(stage=None, fileDIR=None, size=[100,100], sticky="", command=None, column=0, row=0, columnspan=1, rowspan=1):
        try:
            resizedImage = Image.open(fileDIR).resize((size[0], size[1]), Image.Resampling.LANCZOS) # NOTE: .Resampling.LANCZOS allows resizing/changing pixel ratio
            tkImage = ImageTk.PhotoImage(resizedImage)
            button = tk.Button(stage, image=tkImage, command=command, borderwidth=0)
            button.image = tkImage
            button.grid(sticky=sticky, column=column, row=row, columnspan=columnspan, rowspan=rowspan)
            return button
        except:
            print("err: please check file directory and stage")

def imageLinkButton(stage=None, fileDIR=None, size=[100,100], sticky="", column=0, row=0, columnspan=1, rowspan=1, controller=None, page=None, bg="white"):
        try:
            resizedImage = Image.open(fileDIR).resize((size[0], size[1]), Image.Resampling.LANCZOS) # NOTE: .Resampling.LANCZOS allows resizing/changing pixel ratio
            tkImage = ImageTk.PhotoImage(resizedImage)
            button = tk.Button(stage, image=tkImage, command=lambda: controller.show_frame(page), borderwidth=0, bg=bg, activebackground=bg, relief="flat", bd=0, highlightthickness=0)
            button.image = tkImage
            button.grid(sticky=sticky, column=column, row=row, columnspan=columnspan, rowspan=rowspan)
            return button
        except:
            print("err: please check file directory and stage")

def pick_color():
    col = colPicker.askcolor(title="Choose a color") # from tkinter import colorchooser as colPicker
    if col[1]:
        return col[1] # returns hex code
    
def checkBox(stage=None, text="", variable=None, command=None, column=0, row=0, columnspan=1, rowspan=1, sticky=""):
    chkbx = tk.Checkbutton(
            stage, 
            text="Show Grids", 
            variable=variable,
            command=lambda: command
        ).grid(sticky=sticky, column=column, row=row, columnspan=columnspan, rowspan=rowspan)
    return chkbx