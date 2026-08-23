import tkinter as tk

from auth_lib import close_connection, get_connection, save_colors, setup_db
from blog_lib import BlogDB
from pages import (
    Blog,
    ContactPage,
    Courses,
    EditPostPage,
    HomePage,
    NewPostPage,
    SettingsPage,
    SignInPage,
    SignUpPage,
    dbDIR,
)

WIDTH, HEIGHT = 400, 400


def on_closing(mainapp):
    """Handle application closure: save user colors and close database connections."""
    # Save the colors to the database before closing
    if mainapp.logged_in and mainapp.username:
        save_colors(
            mainapp.username,
            [
                mainapp.bg_color_1,
                mainapp.bg_color_2,
                mainapp.header_color_1,
                mainapp.button_color_1,
                mainapp.text_color_1,
            ],
        )
    close_connection()  # Close database connection
    mainapp.blog_db.close_connection()
    mainapp.destroy()


class MainApp(tk.Tk):
    """Scaffold frame for other frames to be placed upon (replacement for root)."""

    def __init__(self, width, height):
        super().__init__()
        # Default user configuration variables
        self.bg_color_1 = "#bdbdbd"
        self.bg_color_2 = "#afafaf"
        self.header_color_1 = "#a0a0a0"
        self.button_color_1 = "#ffffff"
        self.text_color_1 = "#000000"
        self.logged_in_text = None
        self.logged_in = False
        self.username = None

        get_connection(dbDIR / "userInformation.db")
        setup_db()
        self.blog_db = BlogDB(dbDIR / "userInformation.db")
        self.blog_db.setup_db()

        self.current_page = None
        self.title("CodeLog")
        self.geometry(f"{width}x{height}")
        self.state("zoomed")

        self.show_grids = False
        self.show_grids_tk = tk.BooleanVar(value=self.show_grids)

        self.stage = tk.Frame(self)
        self.stage.pack(side="top", fill="both", expand=True)
        self.stage.grid_rowconfigure(0, weight=1, uniform="group1")
        self.stage.grid_columnconfigure(0, weight=1, uniform="group1")

        self.frames = {}
        self.build_all_frames(self.stage)

    def build_all_frames(self, stage):
        """Build all application frames using page classes from pages.py."""
        page_classes = (
            Courses,
            SignUpPage,
            SignInPage,
            Blog,
            EditPostPage,
            NewPostPage,
            ContactPage,
            SettingsPage,
            HomePage,
        )
        for page_class in page_classes:
            page_name = page_class.__name__
            frame = page_class(parent=stage, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, page_name):
        """Show a frame for the given page name."""
        frame = self.frames[page_name]
        if page_name == "Blog" and hasattr(frame, "refresh_posts"):
            frame.refresh_posts()

        frame.tkraise()
        self.current_page = page_name

    def refresh(self):
        """Refresh the application by rebuilding all frames."""
        for frame in self.frames.values():
            frame.destroy()
        self.frames = {}
        self.build_all_frames(self.stage)
        self.show_frame(self.current_page)

    def set_attribute(self, attribute, value):
        """Set an attribute and refresh the application."""
        setattr(self, attribute, value)
        self.refresh()

    def toggle_grid(self):
        """Toggle the grid display on or off."""
        self.show_grids = self.show_grids_tk.get()
        self.refresh()


if __name__ == "__main__":
    main = MainApp(WIDTH, HEIGHT)
    main.protocol("WM_DELETE_WINDOW", lambda: on_closing(main))
    main.mainloop()
    