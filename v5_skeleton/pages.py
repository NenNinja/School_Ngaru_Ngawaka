from pathlib import Path
import sqlite3
import tkinter as tk

from auth_lib import load_colors, register_user, save_colors, verify_login
from nen_tkint_lib import (
    draw_text,
    frame,
    function_button,
    image_link_button,
    link_button,
    pick_color,
)
from pdf_lib import pdf

SCRIPT_DIR = Path(__file__).resolve().parent
ASSET_DIR = SCRIPT_DIR / "assets"
dbDIR = SCRIPT_DIR / "db"


def header(stage, controller):
    """Create a header frame with navigation buttons and user information."""
    header_frame = frame(
        stage,
        controller.header_color_1,
        column=0,
        row=0,
        columnspan=3,
        sticky="nsew",
        column_num=10,
        show_grid=controller.show_grids,
        uniform="hdr_cols",
        propagate=False,
    )

    link_button(
        header_frame,
        "CODELOG",
        controller=controller,
        page="HomePage",
        column=3,
        columnspan=4,
        row=0,
        sticky="",
        bg=controller.header_color_1,
        fg=controller.text_color_1,
        fsize=40,
        fstyle="Arial",
        extra="bold",
        relief="flat",
        bd=0,
        highlightthickness=0,
    )

    if controller.logged_in:
        draw_text(
            header_frame,
            f"Welcome,\n{controller.username}!",
            bg=controller.header_color_1,
            fg=controller.text_color_1,
            column=0,
            row=0,
            sticky="nsew",
            fsize=16,
            columnspan=2,
        )
    else:
        link_button(
            header_frame,
            "Sign In",
            controller=controller,
            page="SignInPage",
            column=0,
            row=0,
            sticky="ew",
            bg=controller.button_color_1,
            fg=controller.text_color_1,
            columnspan=2,
        )

    image_link_button(
        header_frame,
        file_dir=ASSET_DIR / "settingsCog.png",
        size=(50, 50),
        controller=controller,
        page="SettingsPage",
        sticky="news",
        column=9,
        row=0,
        columnspan=1,
        rowspan=1,
        bg=controller.header_color_1,
    )
def draw_grids(controller, stage):
    """Draw grid on the given stage if the show_grids option is enabled."""
    if controller.show_grids:
        for ix in range(3):
            for iy in range(3):
                frame(
                    stage=stage,
                    column=ix,
                    row=iy,
                    sticky="nsew",
                    bg="#ffffff",
                    highlight_color="black",
                    highlight_width=1,
                )


class HomePage(tk.Frame):
    """Home page frame with navigation buttons to other pages."""

    def __init__(self, parent, controller):
        """Initialize the home page and build its interface."""
        super().__init__(parent)
        self.build(controller)

    def build(self, controller):
        """Build the home page layout with navigation buttons."""
        self.configure(bg=controller.bg_color_1)
        self.controller = controller
        self.columnconfigure((0, 2), weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=3)
        self.rowconfigure((1, 2), weight=5)

        draw_grids(controller, self)
        header(self, controller=controller)

        button_frame = frame(
            self,
            bg=controller.bg_color_1,
            column=1,
            row=1,
            rowspan=2,
            sticky="nsew",
            row_num=10,
            show_grid=controller.show_grids,
        )
        link_button(
            button_frame,
            bg=controller.button_color_1,
            fg=controller.text_color_1,
            text="Blog",
            page="Blog",
            controller=controller,
            column=0,
            row=0,
            sticky="news",
            fsize=30,
        )
        link_button(
            button_frame,
            bg=controller.button_color_1,
            fg=controller.text_color_1,
            text="Courses",
            page="Courses",
            controller=controller,
            column=0,
            row=1,
            sticky="news",
            fsize=30,
        )
        link_button(
            button_frame,
            bg=controller.button_color_1,
            fg=controller.text_color_1,
            text="Contact Us",
            page="ContactPage",
            controller=controller,
            column=0,
            row=10,
            sticky="news",
            fsize=30,
        )


class SettingsPage(tk.Frame):
    """Settings page frame to customize application colors."""

    def __init__(self, parent, controller):
        """Initialize the settings page and build its controls."""
        super().__init__(parent)
        self.build(controller)

    def set_color(self, attribute, color):
        """Set a color attribute in the controller and refresh the UI."""
        if color is not None:
            setattr(self.controller, attribute, color)
            self.controller.refresh()

    def reset(self):
        """Reset all color settings to default values and refresh the UI."""
        self.controller.bg_color_1 = "#bdbdbd"
        self.controller.bg_color_2 = "#afafaf"
        self.controller.header_color_1 = "#a0a0a0"
        self.controller.button_color_1 = "#ffffff"
        self.controller.text_color_1 = "#000000"
        self.controller.refresh()

    def build(self, controller):
        """Build the settings page layout with color customization options."""
        self.configure(bg=controller.bg_color_1)
        self.controller = controller
        self.columnconfigure((0, 2), weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=3)
        self.rowconfigure((1, 2), weight=5)

        draw_grids(controller, self)
        header(self, controller=controller)

        settings_frame = frame(
            self,
            bg=controller.bg_color_1,
            column=0,
            row=1,
            rowspan=2,
            columnspan=3,
            sticky="nsew",
            column_num=10,
            row_num=10,
            show_grid=controller.show_grids,
        )

        function_button(
            settings_frame,
            "background:",
            command=lambda: self.set_color("bg_color_1", pick_color()),
            fg=controller.text_color_1,
            column=0,
            row=1,
            bg=controller.button_color_1,
            columnspan=2,
        )
        frame(
            settings_frame,
            bg=controller.bg_color_1,
            column=2,
            row=1,
            sticky="nsew",
            highlight_color="black",
            highlight_width=1,
            padx=10,
        )

        function_button(
            settings_frame,
            "background2: ",
            command=lambda: self.set_color("bg_color_2", pick_color()),
            fg=controller.text_color_1,
            column=0,
            row=2,
            bg=controller.button_color_1,
            columnspan=2,
        )
        frame(
            settings_frame,
            bg=controller.bg_color_2,
            column=2,
            row=2,
            sticky="nsew",
            highlight_color="black",
            highlight_width=1,
            padx=10,
        )

        function_button(
            settings_frame,
            "header: ",
            command=lambda: self.set_color("header_color_1", pick_color()),
            fg=controller.text_color_1,
            column=0,
            row=3,
            bg=controller.button_color_1,
            columnspan=2,
        )
        frame(
            settings_frame,
            bg=controller.header_color_1,
            column=2,
            row=3,
            sticky="nsew",
            highlight_color="black",
            highlight_width=1,
            padx=10,
        )

        function_button(
            settings_frame,
            "buttons: ",
            command=lambda: self.set_color("button_color_1", pick_color()),
            fg=controller.text_color_1,
            column=0,
            row=4,
            bg=controller.button_color_1,
            columnspan=2,
        )
        frame(
            settings_frame,
            bg=controller.button_color_1,
            column=2,
            row=4,
            sticky="nsew",
            highlight_color="black",
            highlight_width=1,
            padx=10,
        )

        function_button(
            settings_frame,
            "text: ",
            command=lambda: self.set_color("text_color_1", pick_color()),
            fg=controller.text_color_1,
            column=0,
            row=5,
            bg=controller.button_color_1,
            columnspan=2,
        )
        frame(
            settings_frame,
            bg=controller.text_color_1,
            column=2,
            row=5,
            sticky="nsew",
            highlight_color="black",
            highlight_width=1,
            padx=10,
        )

        function_button(
            settings_frame,
            "RESET",
            command=self.reset,
            column=0,
            row=9,
            bg="#ffffff",
            columnspan=2,
        )


class SignInPage(tk.Frame):
    """Sign-in page frame for user authentication."""
    def __init__(self, parent, controller):
        """Initialize the sign-in page with input fields and buttons."""
        super().__init__(parent)
        self.login_status = ["", controller.bg_color_1]
        self.build(controller)

    def login(self):
        """Handle user login by verifying credentials and updating the controller state."""
        user_info = verify_login(self.user.get(), self.password.get())
        if user_info:
            print("Login successful!")
            self.controller.logged_in = True
            self.controller.username = user_info["username"]
            self.controller.logged_in_text = True
            col = load_colors(user_info["username"])
            if col:
                self.controller.bg_color_1 = col[0]
                self.controller.bg_color_2 = col[1]
                self.controller.header_color_1 = col[2]
                self.controller.button_color_1 = col[3]
                self.controller.text_color_1 = col[4]
            self.controller.refresh()
            self.controller.show_frame("HomePage")
        else:
            self.controller.logged_in_text = False
            self.controller.refresh()

    def build(self, controller):
        """Build the sign-in page layout with input fields and buttons."""
        self.configure(bg=controller.bg_color_1)
        self.controller = controller
        self.columnconfigure((0, 2), weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=3)
        self.rowconfigure((1, 2), weight=5)
        draw_grids(controller, self)

        header_frame = frame(
            stage=self,
            bg=controller.header_color_1,
            column=0,
            row=0,
            columnspan=3,
            sticky="nsew",
            column_num=10,
            show_grid=controller.show_grids,
            uniform="hdr_cols",
        )
        link_button(
            header_frame,
            "back",
            controller=controller,
            page="HomePage",
            column=0,
            row=0,
            sticky="ew",
            bg=controller.button_color_1,
            padx=50,
        )

        entry_frame = frame(
            self,
            bg=controller.bg_color_1,
            column=1,
            row=1,
            rowspan=2,
            columnspan=1,
            sticky="nsew",
            column_num=2,
            row_num=10,
            show_grid=controller.show_grids,
        )
        draw_text(
            entry_frame,
            "Username:",
            bg=controller.bg_color_1,
            fg=controller.text_color_1,
            column=0,
            row=0,
            sticky="e",
            fsize=20,
            padx=10,
        )
        self.user = tk.Entry(entry_frame, bg="#ffffff", font=("Arial", 14))
        self.user.grid(sticky="w", column=1, row=0, padx=(0, 30))
        draw_text(
            entry_frame,
            "Password:",
            bg=controller.bg_color_1,
            fg=controller.text_color_1,
            column=0,
            row=1,
            sticky="e",
            fsize=20,
            padx=10,
        )
        self.password = tk.Entry(
            entry_frame, bg="#ffffff", show="*", font=("Arial", 14)
        )
        self.password.grid(sticky="w", column=1, row=1, padx=(0, 30))

        if controller.logged_in_text is True:
            draw_text(
                entry_frame,
                "login successful",
                bg=controller.bg_color_1,
                fg="green",
                column=0,
                row=3,
                sticky="nsew",
                fsize=14,
                padx=10,
                columnspan=2,
            )
        elif controller.logged_in_text is False:
            draw_text(
                entry_frame,
                "wrong username or password",
                bg=controller.bg_color_1,
                fg="red",
                column=0,
                row=3,
                sticky="nsew",
                fsize=14,
                padx=10,
                columnspan=2,
            )
        function_button(
            entry_frame,
            "Sign In",
            command=self.login,
            column=0,
            row=2,
            columnspan=2,
            sticky="",
            bg=controller.button_color_1,
        )
        link_button(
            entry_frame,
            "Sign Up",
            controller=controller,
            fg=controller.text_color_1,
            page="SignUpPage",
            column=0,
            row=4,
            columnspan=2,
            sticky="n",
            bg=controller.bg_color_1,
            borderwidth=0,
            relief="flat",
            bd=0,
            highlightthickness=0,
        )


class SignUpPage(tk.Frame):
    """Sign-up page frame for new user registration."""
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.login_status = ["", controller.bg_color_1]
        self.build(controller)

    def sign_up(self):
        """Handle user registration by saving new credentials and colors."""
        if register_user(self.user.get(), self.password.get()):
            self.controller.show_frame("SignInPage")
            save_colors(
                self.user.get(),
                [
                    self.controller.bg_color_1,
                    self.controller.bg_color_2,
                    self.controller.header_color_1,
                    self.controller.button_color_1,
                    self.controller.text_color_1,
                ],
            )
        else:
            print("Username already exists. Please choose a different username.")

    def build(self, controller):
        """Build the sign-up page layout with input fields and buttons."""
        self.configure(bg=controller.bg_color_1)
        self.controller = controller
        self.columnconfigure((0, 2), weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=3)
        self.rowconfigure((1, 2), weight=5)
        draw_grids(controller, self)

        header_frame = frame(
            stage=self,
            bg=controller.header_color_1,
            column=0,
            row=0,
            columnspan=3,
            sticky="nsew",
            column_num=10,
            show_grid=controller.show_grids,
            uniform="hdr_cols",
        )
        link_button(
            header_frame,
            "back",
            controller=controller,
            page="SignInPage",
            column=0,
            row=0,
            sticky="ew",
            bg=controller.button_color_1,
            padx=50,
        )

        entry_frame = frame(
            self,
            bg=controller.bg_color_1,
            column=1,
            row=1,
            rowspan=2,
            columnspan=1,
            sticky="nsew",
            column_num=2,
            row_num=10,
            show_grid=controller.show_grids,
        )
        draw_text(
            entry_frame,
            "Username:",
            bg=controller.bg_color_1,
            fg=controller.text_color_1,
            column=0,
            row=0,
            sticky="e",
            fsize=20,
            padx=10,
        )
        self.user = tk.Entry(entry_frame, bg="#ffffff", font=("Arial", 14))
        self.user.grid(sticky="w", column=1, row=0, padx=(0, 30))
        draw_text(
            entry_frame,
            "Password:",
            bg=controller.bg_color_1,
            fg=controller.text_color_1,
            column=0,
            row=1,
            sticky="e",
            fsize=20,
            padx=10,
        )
        self.password = tk.Entry(
            entry_frame, bg="#ffffff", show="*", font=("Arial", 14)
        )
        self.password.grid(sticky="w", column=1, row=1, padx=(0, 30))

        if controller.logged_in_text is True:
            draw_text(
                entry_frame,
                "login successful",
                bg=controller.bg_color_1,
                fg="green",
                column=0,
                row=3,
                sticky="nsew",
                fsize=14,
                padx=10,
                columnspan=2,
            )
        elif controller.logged_in_text is False:
            draw_text(
                entry_frame,
                "wrong username or password",
                bg=controller.bg_color_1,
                fg="red",
                column=0,
                row=3,
                sticky="nsew",
                fsize=14,
                padx=10,
                columnspan=2,
            )
        function_button(
            entry_frame,
            "Sign Up",
            command=self.sign_up,
            column=0,
            row=2,
            columnspan=2,
            sticky="",
            bg=controller.button_color_1,
        )


class Courses(tk.Frame):
    """Courses page frame to display course-related content."""

    def __init__(self, parent, controller):
        """Initialize the courses page and build its layout."""
        super().__init__(parent)
        self.build(controller)

    def build(self, controller):
        """Build the courses page layout with navigation buttons."""
        self.configure(bg=controller.bg_color_1)
        self.controller = controller
        self.columnconfigure((0, 2), weight=1, uniform="group1")
        self.columnconfigure(1, weight=2, uniform="group1")
        self.rowconfigure(0, weight=3, uniform="group1")
        self.rowconfigure((1, 2), weight=5, uniform="group1")
        draw_grids(controller, self)
        header(self, controller=controller)

        buttons_frame = frame(
            self,
            bg=controller.bg_color_2,
            column=0,
            row=1,
            rowspan=2,
            sticky="nsew",
            row_num=10,
            show_grid=controller.show_grids,
        )

        v_scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        pdf_viewer_canvas = tk.Canvas(
            self, bg="gray", yscrollcommand=v_scrollbar.set, width=1, height=1
        )
        pdf_viewer_canvas.grid(
            column=1, columnspan=1, row=1, rowspan=2, sticky="nesw"
        )
        v_scrollbar.config(command=pdf_viewer_canvas.yview)
        v_scrollbar.grid(sticky="nws", column=2, row=1, rowspan=2)

        function_button(
            self,
            "← prev",
            bg=controller.button_color_1,
            fg=controller.text_color_1,
            command=lambda: pdf.prev_page(pdf_viewer_canvas, cur_page_text),
            column=2,
            row=1,
            sticky="n",
            padx=(0, 200),
        )
        cur_page_text = draw_text(
            self,
            "Page: 0 / 0",
            bg=controller.bg_color_1,
            fg=controller.text_color_1,
            column=2,
            row=1,
            sticky="n",
        )
        function_button(
            self,
            "next →",
            bg=controller.button_color_1,
            fg=controller.text_color_1,
            command=lambda: pdf.next_page(pdf_viewer_canvas, cur_page_text),
            column=2,
            row=1,
            sticky="n",
            padx=(200, 0),
        )

        function_button(
            buttons_frame,
            "print()",
            sticky="nesw",
            command=lambda: pdf.open_pdf(
                ASSET_DIR / "python_print_explained.pdf",
                pdf_viewer_canvas,
                cur_page_text,
            ),
            row=0,
        )
        function_button(
            buttons_frame,
            "def",
            sticky="nesw",
            command=lambda: pdf.open_pdf(
                ASSET_DIR / "python_def_explained.pdf",
                pdf_viewer_canvas,
                cur_page_text,
            ),
            row=1,
        )


class Blog(tk.Frame):
    """Blog page frame to display and manage blog posts."""
    def __init__(self, parent, controller):
        """Initialize the blog page with a post selection frame and a content display area."""
        super().__init__(parent)
        self.current_selected_title = None
        self.build(controller)

    def display_post(self, title):
        """Display the content of the selected blog post 
        and show the edit button if the user is the author."""
        self.current_selected_title = title
        post = self.controller.blog_db.get_post(title)

        self.post_content_text.config(state="normal")
        self.post_content_text.delete("1.0", tk.END)

        if post:
            username, title_text, content, timestamp = post
            formatted_text = (
                f"Title: {title_text}\n"
                f"Author: {username}\n"
                f"Date: {timestamp}\n\n"
                f"{content}"
            )
            self.post_content_text.insert(tk.END, formatted_text)

            if (
                self.controller.logged_in
                and self.controller.username == username
            ):
                self.edit_btn.grid(column=0, row=0, sticky="e", padx=5)
            else:
                self.edit_btn.grid_forget()
        else:
            self.post_content_text.insert(tk.END, "Post not found.")
            self.edit_btn.grid_forget()

        self.post_content_text.config(state="disabled")

    def open_edit_page(self):
        """Open the edit post page with the currently selected post's data."""
        if self.current_selected_title:
            edit_frame = self.controller.frames.get("EditPostPage")
            if edit_frame:
                edit_frame.load_post_data(self.current_selected_title)
                self.controller.show_frame("EditPostPage")

    def refresh_posts(self):
        """Clears existing buttons and rebuilds the post list from the database."""
        for child in self.select_frame.winfo_children():
            child.destroy()

        posts = self.controller.blog_db.get_all_posts()
        for idx, post in enumerate(posts):
            function_button(
                self.select_frame,
                f"{post[1]} by {post[0]}",
                bg=self.controller.bg_color_2,
                fg=self.controller.text_color_1,
                column=0,
                row=idx,
                sticky="nsew",
                padx=10,
                pady=5,
                command=lambda title=post[1]: self.display_post(title),
            )

    def build(self, controller):
        """Build the blog page layout with a post selection frame and a content display area."""
        self.configure(bg=controller.bg_color_1)
        self.controller = controller
        self.columnconfigure((0, 2), weight=1, uniform="group1")
        self.columnconfigure(1, weight=1, uniform="group1")
        self.rowconfigure(0, weight=3, uniform="group1")
        self.rowconfigure((1, 2), weight=5, uniform="group1")

        draw_grids(controller, self)
        header(self, controller=controller)

        blog_frame = frame(
            self,
            bg=controller.bg_color_1,
            column=0,
            row=1,
            rowspan=2,
            columnspan=3,
            sticky="nsew",
            column_num=10,
            row_num=10,
            show_grid=controller.show_grids,
            uniform="blog_main",
        )

        self.select_frame = frame(
            blog_frame,
            bg=controller.bg_color_2,
            column=0,
            row=0,
            rowspan=10,
            columnspan=3,
            sticky="nsew",
            column_num=1,
            row_num=10,
            show_grid=controller.show_grids,
            uniform="blog_select",
        )

        top_bar_frame = tk.Frame(blog_frame, bg=controller.bg_color_1)
        top_bar_frame.grid(
            column=3, row=0, columnspan=7, sticky="nsew", padx=5, pady=5
        )

        self.edit_btn = tk.Button(
            top_bar_frame,
            text="Edit Post",
            command=self.open_edit_page,
            bg=controller.button_color_1,
            fg=controller.text_color_1,
            font=("Arial", 12),
            bd=1,
            relief="raised",
        )

        if controller.logged_in:
            new_post_btn = tk.Button(
                top_bar_frame,
                text="New Post +",
                command=lambda: controller.show_frame("NewPostPage"),
                bg=controller.button_color_1,
                fg=controller.text_color_1,
                font=("Arial", 12),
                bd=1,
                relief="raised",
            )
            new_post_btn.grid(column=1, row=0, sticky="e", padx=5)
        else:
            draw_text(
                top_bar_frame,
                "Sign in to post",
                bg=controller.bg_color_1,
                fg=controller.text_color_1,
                column=0,
                row=0,
                sticky="e",
                fsize=11,
            )

        display_container = frame(
            blog_frame,
            bg=controller.bg_color_1,
            column=3,
            row=1,
            rowspan=9,
            columnspan=7,
            sticky="nsew",
        )
        display_container.columnconfigure(0, weight=1)
        display_container.rowconfigure(0, weight=1)

        self.post_content_text = tk.Text(
            display_container,
            bg=controller.bg_color_1,
            fg=controller.text_color_1,
            font=("Arial", 14),
            wrap="word",
            bd=0,
            highlightthickness=0,
        )
        self.post_content_text.grid(
            column=0, row=0, sticky="nsew", padx=10, pady=10
        )
        self.post_content_text.insert(
            tk.END, "Select a post to view its content:"
        )
        self.post_content_text.config(state="disabled")

        self.refresh_posts()


class EditPostPage(tk.Frame):
    """Page for editing an existing blog post."""

    def __init__(self, parent, controller):
        """Initialize the edit post page and build its form."""
        super().__init__(parent)
        self.old_title = None
        self.build(controller)

    def load_post_data(self, title):
        """Load the selected post's title and content into the form fields."""
        self.old_title = title
        post = self.controller.blog_db.get_post(title)
        if post:
            _, post_title, content, _ = post
            self.title_entry.delete(0, tk.END)
            self.title_entry.insert(0, post_title)

            self.content_entry.delete("1.0", tk.END)
            self.content_entry.insert(tk.END, content)
            self.status_label.config(text="")

    def save_changes(self):
        """Save any edits made to the selected post."""
        new_title = self.title_entry.get().strip()
        new_content = self.content_entry.get("1.0", tk.END).strip()

        if not new_title or not new_content:
            self.status_label.config(
                text="Title and content cannot be empty.", fg="red"
            )
            return

        try:
            self.controller.blog_db.edit_post(
                self.controller.username, self.old_title, new_title, new_content
            )
            self.controller.show_frame("Blog")
        except sqlite3.Error as e:
            self.status_label.config(text=f"Error updating post: {e}", fg="red")

    def delete_current_post(self):
        """Delete the currently loaded post after confirming ownership."""
        try:
            self.controller.blog_db.delete_post(
                self.controller.username, self.old_title
            )
            self.controller.show_frame("Blog")
        except sqlite3.Error as e:
            self.status_label.config(text=f"Error deleting post: {e}", fg="red")

    def build(self, controller):
        """Build the edit post form with title, content, and action buttons."""
        self.configure(bg=controller.bg_color_1)
        self.controller = controller
        self.columnconfigure((0, 2), weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=3)
        self.rowconfigure((1, 2), weight=5)

        draw_grids(controller, self)

        header_frame = frame(
            stage=self,
            bg=controller.header_color_1,
            column=0,
            row=0,
            columnspan=3,
            sticky="nsew",
            column_num=10,
            show_grid=controller.show_grids,
            uniform="hdr_cols",
        )
        link_button(
            header_frame,
            "back",
            controller=controller,
            page="Blog",
            column=0,
            row=0,
            sticky="ew",
            bg=controller.button_color_1,
            padx=50,
        )

        form_frame = frame(
            self,
            bg=controller.bg_color_1,
            column=1,
            row=1,
            rowspan=2,
            columnspan=1,
            sticky="nsew",
            column_num=2,
            row_num=10,
            show_grid=controller.show_grids,
        )

        draw_text(
            form_frame,
            "Edit Post",
            bg=controller.bg_color_1,
            fg=controller.text_color_1,
            column=0,
            row=0,
            columnspan=2,
            sticky="n",
            fsize=22,
            extra="bold",
        )

        draw_text(
            form_frame,
            "Title:",
            bg=controller.bg_color_1,
            fg=controller.text_color_1,
            column=0,
            row=1,
            columnspan=2,
            sticky="w",
            fsize=14,
        )
        self.title_entry = tk.Entry(form_frame, bg="#ffffff", font=("Arial", 14))
        self.title_entry.grid(sticky="ew", column=0, row=2, columnspan=2, padx=10)

        draw_text(
            form_frame,
            "Content:",
            bg=controller.bg_color_1,
            fg=controller.text_color_1,
            column=0,
            row=3,
            columnspan=2,
            sticky="w",
            fsize=14,
        )
        self.content_entry = tk.Text(
            form_frame, bg="#ffffff", font=("Arial", 12), wrap="word", height=6
        )
        self.content_entry.grid(
            sticky="nsew", column=0, row=4, rowspan=3, columnspan=2, padx=10
        )

        self.status_label = draw_text(
            form_frame,
            "",
            bg=controller.bg_color_1,
            fg="red",
            column=0,
            row=7,
            columnspan=2,
            sticky="n",
            fsize=12,
        )

        function_button(
            form_frame,
            "Save Changes",
            command=self.save_changes,
            column=0,
            row=8,
            sticky="ew",
            bg=controller.button_color_1,
            fg=controller.text_color_1,
            fsize=12,
            padx=5,
        )
        function_button(
            form_frame,
            "Delete Post",
            command=self.delete_current_post,
            column=1,
            row=8,
            sticky="ew",
            bg="#ff5555",
            fg="white",
            fsize=12,
            padx=5,
        )


class NewPostPage(tk.Frame):
    """Page for creating and publishing a new blog post."""

    def __init__(self, parent, controller):
        """Initialize the new post page and build its form."""
        super().__init__(parent)
        self.build(controller)

    def publish_post(self):
        """Publish the entered post for the current logged-in user."""
        title = self.title_entry.get().strip()
        content = self.content_entry.get("1.0", tk.END).strip()

        if not title or not content:
            self.status_label.config(
                text="Title and content cannot be empty.", fg="red"
            )
            return

        if not self.controller.logged_in or not self.controller.username:
            self.status_label.config(
                text="You must be logged in to post.", fg="red"
            )
            return

        try:
            self.controller.blog_db.new_post(
                self.controller.username, title, content
            )
            self.status_label.config(
                text="Post published successfully!", fg="green"
            )
            self.title_entry.delete(0, tk.END)
            self.content_entry.delete("1.0", tk.END)
            self.controller.refresh()
            self.controller.show_frame("Blog")
        except sqlite3.IntegrityError:
            self.status_label.config(
                text="A post with this title already exists.", fg="red"
            )
        except sqlite3.Error as e:
            self.status_label.config(text=f"Error: {e}", fg="red")

    def build(self, controller):
        """Build the new post form with title and content fields."""
        self.configure(bg=controller.bg_color_1)
        self.controller = controller
        self.columnconfigure((0, 2), weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=3)
        self.rowconfigure((1, 2), weight=5)

        draw_grids(controller, self)

        header_frame = frame(
            stage=self,
            bg=controller.header_color_1,
            column=0,
            row=0,
            columnspan=3,
            sticky="nsew",
            column_num=10,
            show_grid=controller.show_grids,
            uniform="hdr_cols",
        )
        link_button(
            header_frame,
            "back",
            controller=controller,
            page="Blog",
            column=0,
            row=0,
            sticky="ew",
            bg=controller.button_color_1,
            padx=50,
        )

        form_frame = frame(
            self,
            bg=controller.bg_color_1,
            column=1,
            row=1,
            rowspan=2,
            columnspan=1,
            sticky="nsew",
            column_num=1,
            row_num=10,
            show_grid=controller.show_grids,
        )

        draw_text(
            form_frame,
            "Create New Post",
            bg=controller.bg_color_1,
            fg=controller.text_color_1,
            column=0,
            row=0,
            sticky="n",
            fsize=22,
            extra="bold",
        )

        draw_text(
            form_frame,
            "Title:",
            bg=controller.bg_color_1,
            fg=controller.text_color_1,
            column=0,
            row=1,
            sticky="w",
            fsize=14,
        )
        self.title_entry = tk.Entry(form_frame, bg="#ffffff", font=("Arial", 14))
        self.title_entry.grid(sticky="ew", column=0, row=2, padx=10)

        draw_text(
            form_frame,
            "Content:",
            bg=controller.bg_color_1,
            fg=controller.text_color_1,
            column=0,
            row=3,
            sticky="w",
            fsize=14,
        )

        self.content_entry = tk.Text(
            form_frame, bg="#ffffff", font=("Arial", 12), wrap="word", height=6
        )
        self.content_entry.grid(
            sticky="nsew", column=0, row=4, rowspan=3, padx=10
        )

        self.status_label = draw_text(
            form_frame,
            "",
            bg=controller.bg_color_1,
            fg="red",
            column=0,
            row=7,
            sticky="n",
            fsize=12,
        )

        function_button(
            form_frame,
            "Publish Post",
            command=self.publish_post,
            column=0,
            row=8,
            sticky="",
            bg=controller.button_color_1,
            fg=controller.text_color_1,
            fsize=14,
        )


class ContactPage(tk.Frame):
    """Page showing contact information for the application."""

    def __init__(self, parent, controller):
        """Initialize the contact page and build its layout."""
        super().__init__(parent)
        self.build(controller)

    def build(self, controller):
        """Build the contact page with the header and contact details."""
        self.configure(bg=controller.bg_color_1)
        self.controller = controller
        self.columnconfigure((0, 2), weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=3)
        self.rowconfigure((1, 2), weight=5)

        draw_grids(controller, self)
        header(self, controller=controller)

        draw_text(
            self,
            "+61 ##########",
            bg=controller.bg_color_1,
            fg=controller.text_color_1,
            column=1,
            row=1,
            sticky="n",
            fsize=30,
        )