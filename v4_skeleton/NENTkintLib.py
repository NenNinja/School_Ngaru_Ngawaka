import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import colorchooser as colPicker
from pathlib import Path

def frame(stage=None, bg="#ffffff", column=0, row=0, columnspan=1, rowspan=1, sticky="", columnNum=0, rowNum=0, showGrid=False, highLightColor="black", highLightWidth=0, padx=0, pady=0, uniform="group1", propagate=False):
    frame1 = tk.Frame(
        stage,
        bg=bg, 
        highlightbackground=highLightColor, 
        highlightthickness=highLightWidth,
        )
    frame1.grid(
        column=column, 
        row=row, 
        columnspan=columnspan, 
        rowspan=rowspan, 
        sticky=sticky,
        padx=padx,
        pady=pady
        )
    
    # Configure columns
    cols = columnNum if columnNum > 0 else 1
    for i in range(cols): 
        frame1.columnconfigure(i, weight=1, uniform=uniform)

    # Configure rows
    rows = rowNum if rowNum > 0 else 1
    for i in range(rows):
        frame1.rowconfigure(i, weight=1, uniform=uniform)

    frame1.grid_propagate(propagate)
    
    if showGrid:
        for ix in range(cols):
            for iy in range(rows):
                frame(
                    stage=frame1,
                    column=ix, row=iy, 
                    sticky="nsew", 
                    bg="#ffffff",
                    highLightColor="black",
                    highLightWidth=1,
                    uniform=f"debug_{uniform}"
                    )
                
    return frame1

def drawText(stage=None, text="", bg="white", fg="black", fstyle="Arial", fsize=14, extra="normal", padx=0, pady=0, sticky="", column=0, row=0, columnspan=1, rowspan=1):
    label = tk.Label(
        stage, 
        text=text, 
        bg=bg, 
        fg=fg, 
        font=(fstyle, fsize, extra)
        )
    label.grid(
            sticky=sticky, 
            column=column, row=row, 
            columnspan=columnspan, rowspan=rowspan, 
        padx=padx, pady=pady
            )
    return label # return label so you can use it to change the text later (eg. label.config(text="new text")) (for dynamic text like score, timer, etc.)

def functionButton(stage=None, text="", bg="white", fg="black", fstyle="Arial", fsize=14, extra="normal", padx=0, pady=0, sticky="", command=None, column=0, row=0, columnspan=1, rowspan=1):
    button = tk.Button(
        stage, 
        text=text, 
        bg=bg, 
        fg=fg, 
        font=(fstyle, fsize, extra),  
        command=command
        )
    button.grid(
            sticky=sticky, 
            column=column, row=row, 
            padx=padx, pady=pady,
            columnspan=columnspan, rowspan=rowspan
            )
    return button

def linkButton(stage=None, text="", bg="white", fg="black", fstyle="Arial", fsize=14, extra="normal", padx=0, pady=0, sticky="", controller=None, page=None, column=0, row=0, columnspan=1, rowspan=1, activebackground=None, borderwidth=1, relief="raised", bd=1, highlightthickness=0):
    button = tk.Button(
        stage, 
        text=text, 
        bg=bg, 
        fg=fg, 
        font=(fstyle, fsize, extra), 
        command=lambda: controller.show_frame(page),
        activebackground=activebackground,
        borderwidth=borderwidth,
        relief=relief,
        bd=bd,
        highlightthickness=highlightthickness
        )
    button.grid(
            sticky=sticky, 
            column=column, 
            row=row, 
            columnspan=columnspan, 
            rowspan=rowspan,
            padx=padx, pady=pady, 
            )
    button.grid_propagate(False)
    return button

def drawEntry(stage=None, bg="white", fg="black", fstyle="Arial", fsize=14, extra="normal", padx=0, pady=0, sticky="", column=0, row=0, columnspan=1, rowspan=1):
    entry = tk.Entry(
        stage, 
        bg=bg, 
        fg=fg, 
        font=(fstyle, fsize, extra)
        )
    entry.grid(
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
        )
    radio.grid(
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
            resizedImage = Image.open(fileDIR).resize((size[0], size[1]), Image.Resampling.LANCZOS) # .Resampling.LANCZOS allows resizing/changing pixel ratio
            tkImage = ImageTk.PhotoImage(resizedImage)
            imageLabel = tk.Label(stage, image=tkImage).grid(sticky=sticky, column=column, row=row, columnspan=columnspan, rowspan=rowspan)
            imageLabel.image = tkImage
            return imageLabel
        except:
             print("err: please check file directory and stage")

def imageCommandButton(stage=None, fileDIR=None, size=[100,100], sticky="", command=None, column=0, row=0, columnspan=1, rowspan=1):
        try:
            resizedImage = Image.open(fileDIR).resize((size[0], size[1]), Image.Resampling.LANCZOS)
            tkImage = ImageTk.PhotoImage(resizedImage)
            button = tk.Button(stage, image=tkImage, command=command, borderwidth=0)
            button.image = tkImage
            button.grid(sticky=sticky, column=column, row=row, columnspan=columnspan, rowspan=rowspan)
            return button
        except:
            print("err: please check file directory and stage")

def imageLinkButton(stage=None, fileDIR=None, size=[100,100], sticky="", column=0, row=0, columnspan=1, rowspan=1, controller=None, page=None, bg="white"):
        try:
            resizedImage = Image.open(fileDIR).resize((size[0], size[1]), Image.Resampling.LANCZOS)
            tkImage = ImageTk.PhotoImage(resizedImage)
            button = tk.Button(stage, image=tkImage, command=lambda: controller.show_frame(page), borderwidth=0, bg=bg, activebackground=bg, relief="flat", bd=0, highlightthickness=0)
            button.image = tkImage
            button.grid(sticky=sticky, column=column, row=row, columnspan=columnspan, rowspan=rowspan)
            return button
        except:
            print("err: please check file directory and stage")

def pickColor():
    col = colPicker.askcolor(title="Choose a color") # from tkinter import colorchooser as colPicker
    if col[1]:
        return col[1] # returns hex code
    
def checkBox(stage=None, text="", variable=None, command=None, column=0, row=0, columnspan=1, rowspan=1, sticky=""):
    chkbx = tk.Checkbutton(
            stage, 
            text="Show Grids", 
            variable=variable,
            command=command
        ).grid(sticky=sticky, column=column, row=row, columnspan=columnspan, rowspan=rowspan)
    return chkbx