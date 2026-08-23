import tkinter as tk
from tkinter import colorchooser as col_picker
from tkinter import ttk

from PIL import Image, ImageTk

# Author: Ngaru Ngawaka / Nen_Ninja

def frame(
    stage=None,
    bg="#ffffff",
    column=0,
    row=0,
    columnspan=1,
    rowspan=1,
    sticky="",
    column_num=0,
    row_num=0,
    show_grid=False,
    highlight_color="black",
    highlight_width=0,
    padx=0,
    pady=0,
    uniform="group1",
    propagate=False,
):
    """Create a frame with specified properties and optional grid layout."""
    frame1 = tk.Frame(
        stage,
        bg=bg,
        highlightbackground=highlight_color,
        highlightthickness=highlight_width,
    )
    frame1.grid(
        column=column,
        row=row,
        columnspan=columnspan,
        rowspan=rowspan,
        sticky=sticky,
        padx=padx,
        pady=pady,
    )

    cols = column_num if column_num > 0 else 1
    for i in range(cols):
        frame1.columnconfigure(i, weight=1, uniform=uniform)

    rows = row_num if row_num > 0 else 1
    for i in range(rows):
        frame1.rowconfigure(i, weight=1, uniform=uniform)

    frame1.grid_propagate(propagate)

    if show_grid:
        for ix in range(cols):
            for iy in range(rows):
                frame(
                    stage=frame1,
                    column=ix,
                    row=iy,
                    sticky="nsew",
                    bg="#ffffff",
                    highlight_color="black",
                    highlight_width=1,
                    uniform=f"debug_{uniform}",
                )

    return frame1


def draw_text(
    stage=None,
    text="",
    bg="white",
    fg="black",
    fstyle="Arial",
    fsize=14,
    extra="normal",
    padx=0,
    pady=0,
    sticky="",
    column=0,
    row=0,
    columnspan=1,
    rowspan=1,
):
    """Create a label with specified properties."""
    label = tk.Label(stage, text=text, bg=bg, fg=fg, font=(fstyle, fsize, extra))
    label.grid(
        sticky=sticky,
        column=column,
        row=row,
        columnspan=columnspan,
        rowspan=rowspan,
        padx=padx,
        pady=pady,
    )
    return label


def function_button(
    stage=None,
    text="",
    bg="white",
    fg="black",
    fstyle="Arial",
    fsize=14,
    extra="normal",
    padx=0,
    pady=0,
    sticky="",
    command=None,
    column=0,
    row=0,
    columnspan=1,
    rowspan=1,
):
    """Create a button with specified properties and an associated command."""
    button = tk.Button(
        stage,
        text=text,
        bg=bg,
        fg=fg,
        font=(fstyle, fsize, extra),
        command=command,
    )
    button.grid(
        sticky=sticky,
        column=column,
        row=row,
        padx=padx,
        pady=pady,
        columnspan=columnspan,
        rowspan=rowspan,
    )
    return button


def link_button(
    stage=None,
    text="",
    bg="white",
    fg="black",
    fstyle="Arial",
    fsize=14,
    extra="normal",
    padx=0,
    pady=0,
    sticky="",
    controller=None,
    page=None,
    column=0,
    row=0,
    columnspan=1,
    rowspan=1,
    activebackground=None,
    borderwidth=1,
    relief="raised",
    bd=1,
    highlightthickness=0,
):
    """Create a button that links to another page in the application."""
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
        highlightthickness=highlightthickness,
    )
    button.grid(
        sticky=sticky,
        column=column,
        row=row,
        columnspan=columnspan,
        rowspan=rowspan,
        padx=padx,
        pady=pady,
    )
    button.grid_propagate(False)
    return button


def draw_entry(
    stage=None,
    bg="white",
    fg="black",
    fstyle="Arial",
    fsize=14,
    extra="normal",
    padx=0,
    pady=0,
    sticky="",
    column=0,
    row=0,
    columnspan=1,
    rowspan=1,
):
    """Create an entry widget with specified properties."""
    entry = tk.Entry(stage, bg=bg, fg=fg, font=(fstyle, fsize, extra))
    entry.grid(
        sticky=sticky,
        column=column,
        row=row,
        columnspan=columnspan,
        rowspan=rowspan,
        padx=padx,
        pady=pady,
    )
    return entry


def radio_button(
    stage=None,
    text="",
    variable=None,
    value=None,
    padx=0,
    pady=0,
    sticky="",
    column=0,
    row=0,
    columnspan=1,
    rowspan=1,
):
    """Create a radio button with specified properties."""
    radio = ttk.Radiobutton(stage, text=text, variable=variable, value=value)
    radio.grid(
        sticky=sticky,
        column=column,
        row=row,
        columnspan=columnspan,
        rowspan=rowspan,
        padx=padx,
        pady=pady,
    )
    return radio


def render_image(
    stage=None,
    file_dir=None,
    size=(100, 100),
    sticky="",
    column=0,
    row=0,
    columnspan=1,
    rowspan=1,
):
    """Create a label with an image loaded from the specified 
    file directory and resized to the given size."""
    try:
        resized_image = Image.open(file_dir).resize(
            (size[0], size[1]), Image.Resampling.LANCZOS
        )
        tk_image = ImageTk.PhotoImage(resized_image)
        image_label = tk.Label(stage, image=tk_image)
        image_label.grid(
            sticky=sticky,
            column=column,
            row=row,
            columnspan=columnspan,
            rowspan=rowspan,
        )
        image_label.image = tk_image
        return image_label
    except (OSError, ValueError, tk.TclError) as err:
        print(f"Error loading image: {err}")


def image_command_button(
    stage=None,
    file_dir=None,
    size=(100, 100),
    sticky="",
    command=None,
    column=0,
    row=0,
    columnspan=1,
    rowspan=1,
):
    """Create a button with an image loaded from the specified 
    file directory and resized to the given size, 
    which executes a command when clicked."""
    try:
        resized_image = Image.open(file_dir).resize(
            (size[0], size[1]), Image.Resampling.LANCZOS
        )
        tk_image = ImageTk.PhotoImage(resized_image)
        button = tk.Button(stage, image=tk_image, command=command, borderwidth=0)
        button.image = tk_image
        button.grid(
            sticky=sticky,
            column=column,
            row=row,
            columnspan=columnspan,
            rowspan=rowspan,
        )
        return button
    except (OSError, ValueError, tk.TclError) as err:
        print(f"Error loading image button: {err}")


def image_link_button(
    stage=None,
    file_dir=None,
    size=(100, 100),
    sticky="",
    column=0,
    row=0,
    columnspan=1,
    rowspan=1,
    controller=None,
    page=None,
    bg="white",
):
    """Create a button with an image loaded 
    from the specified file directory 
    and resized to the given size, 
    which links to another page in the application."""
    try:
        resized_image = Image.open(file_dir).resize(
            (size[0], size[1]), Image.Resampling.LANCZOS
        )
        tk_image = ImageTk.PhotoImage(resized_image)
        button = tk.Button(
            stage,
            image=tk_image,
            command=lambda: controller.show_frame(page),
            borderwidth=0,
            bg=bg,
            activebackground=bg,
            relief="flat",
            bd=0,
            highlightthickness=0,
        )
        button.image = tk_image
        button.grid(
            sticky=sticky,
            column=column,
            row=row,
            columnspan=columnspan,
            rowspan=rowspan,
        )
        return button
    except (OSError, ValueError, tk.TclError) as err:
        print(f"Error loading image link button: {err}")


def pick_color():
    """Open a color picker dialog and return the selected color in hexadecimal format."""
    col = col_picker.askcolor(title="Choose a color")
    if col[1]:
        return col[1]


def check_box(
    stage=None,
    text="",
    variable=None,
    command=None,
    column=0,
    row=0,
    columnspan=1,
    rowspan=1,
    sticky="",
):
    """Create a checkbutton with specified properties and an associated command."""
    chkbx = tk.Checkbutton(stage, text=text, variable=variable, command=command)
    chkbx.grid(
        sticky=sticky,
        column=column,
        row=row,
        columnspan=columnspan,
        rowspan=rowspan,
    )
    return chkbx