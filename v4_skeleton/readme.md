# CODELOG python programming helper

A tkinter desktop application that offers services such as blogging and 
informative cources to help its user learn tkinter. When starting you cant
post or track progress until you sign in, by signing in you can track your
posts, comments and progress in the course.

## How to run

You need Python 3 with tkinter (tkinter ships with most standard Python
installs on Windows and macOS; on some Linux systems you install it separately,
e.g. `sudo apt install python3-tk`).

From inside the project folder:

```
python main.py
```

(or `python3 main.py` depending on your system).

## File structure

| File         | Role        | Plain-English description                                               |
|--------------|-------------|-------------------------------------------------------------------------|
| `main.py`    | Entry point | Builds the objects and starts the program. Run this one.                |
| `pages.py`   | View        | Builds each page and holds page specific functions.                     |
| `authLib.py` | library     | Defines commonly used functions such as labels, buttons and frames.     |
| `authLib.py` | library     | Defines functions used in login authentication and database interaction |
| `pdfLib.py`  | library     | Handles pdf reading and displaying                                      |

## How the pieces fit together
├─
└─ 
```
main.py
  └─ Makes MAIN() class which handles all pages and page switching
     └─ Makes a list of pages                                         (page classes)
        ├─ Accesses authLib.py to log in or register new user
        ├─ Accesses pdfLib.py to open, read and display PDF files for courses
        └─ Defines each "page" as a class that inherits attributes of tk.frame
```

The settings page currently alters any colors in the program
can also be changed in the config.txt file (incase you cant make your way back to the settings page)
and settings button and RESET button on the page will always be visable incase user messes up the colors

!WARNING!
if you alter the config file it will not run
if that happens copy and past this back into the *config.txt* file:
=========================
backgroundColor1=#bdbdbd
backgroundColor2=#afafaf
headerColor1=#a0a0a0
buttonColor1=#ffffff
textColor1=#000000
=========================