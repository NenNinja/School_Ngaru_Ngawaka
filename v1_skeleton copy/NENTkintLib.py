from logging import root
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import colorchooser as colPicker
from pathlib import Path

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

def frame(stage=None, bg="#ffffff", column=0, row=0, columnspan=1, rowspan=1, sticky="", columnNum=0, rowNum=0, highLightColor="black", highLightWidth=0):
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
        command=command
        ).grid(
            sticky=sticky, 
            column=column, row=row, 
            columnspan=columnspan, rowspan=rowspan
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
