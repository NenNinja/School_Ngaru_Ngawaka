# CODELOG Python Programming Helper

A Tkinter desktop application that offers services such as blogging and informative courses to help users learn Tkinter. When starting, users cannot post or track progress until signing in; authentication allows tracking posts, comments, and learning progress.

## How to Run

You need Python 3 with Tkinter installed. (Tkinter ships with most standard Python installs on Windows and macOS; on some Linux distributions, install it separately via `sudo apt install python3-tk`).

1. Clone or download the project folder.
2. Install required third-party dependencies:
   ```bash
   pip install pillow PyMuPDF
   ```
3. Run the application from inside the project directory:
   ```bash
   python main.py
   ```
   *(or `python3 main.py` depending on your environment)*

## File Structure

| File | Role | Plain-English Description |
|---|---|---|
| `main.py` | Entry point | Builds application objects, initializes database connections, and launches the main window loop. |
| `pages.py` | View layer | Defines UI frames (HomePage, Blog, Settings, Courses, etc.) and handles page navigation events. |
| `nen_tkint_lib.py` | UI Library | Custom wrapper functions to create styled Tkinter widgets (buttons, frames, entry boxes, images). |
| `auth_lib.py` | Auth Library | Manages user registration, PBKDF2 password hashing, login verification, and color theme loading/saving. |
| `blog_lib.py` | Database | `BlogDB` class managing SQLite database operations (CRUD) for blog posts. |
| `pdf_lib.py` | Viewer Library | `PDFHandler` class using PyMuPDF and Pillow to render course PDF materials on a Tkinter canvas. |

## Architecture & Data Flow

```text
main.py
  └─ MainApp (tk.Tk)
     ├─ Connects to SQLite DB (userInformation.db)
     ├─ Instantiates Auth & Blog services (auth_lib.py, blog_lib.py)
     ├─ Constructs Page Views (pages.py)
     │  ├─ Imports custom widget components from nen_tkint_lib.py
     │  ├─ Authenticates credentials & loads saved UI color themes
     │  ├─ Performs blog post actions via BlogDB instance
     │  └─ Displays course materials via PDFHandler (pdf_lib.py)
     └─ Handles main execution loop and application cleanup on close
```

## Settings & Custom Themes

Color themes can be adjusted dynamically in the **Settings** view. When logged in, your color theme preference is automatically persisted to the SQLite database and restored upon future sign-ins. A **RESET** button is always available on the Settings page to restore default application colors.

## Pep8 conventions & Pylint

When finishing the project I massively reformatted my program in v5.
This was done with the use of **Pylint** to ensure accurate and clear formatting.

## Further information

For anymore direct informations or questions please either contact my teacher Ms Bharani
or contact me directly at 25458@student.macleans.school.nz

- Ngaru Ngawaka