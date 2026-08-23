from NENTkintLib import *
from authLib import *
from pdfLib import *
from blogLib import *

scriptDIR = Path(__file__).resolve().parent
assetDIR = scriptDIR/"assets"
dbDIR = scriptDIR/"db"

def header(stage, controller):
    # Lock header columns with a unique uniform group name
    headerFrame = frame(stage, controller.headerColor1, column=0, row=0, columnspan=3, sticky="nsew", columnNum=10, showGrid=controller.showGrids, uniform="hdr_cols", propagate=False)
    
    linkButton(headerFrame, "CODELOG", controller=controller, page="HomePage", column=3, columnspan=4, row=0, sticky="", bg=controller.headerColor1, fg=controller.textColor1, fsize=40, fstyle="Arial", extra="bold", relief="flat", bd=0, highlightthickness=0)
    
    if controller.loggedIn:
        # Reduced font size from 30 to 16 so the login string does not force column 0 to expand
        drawText(headerFrame, f"Welcome,\n{controller.username}!", bg=controller.headerColor1, fg=controller.textColor1, column=0, row=0, sticky="nsew", fsize=16, columnspan=2)
    else:
        linkButton(headerFrame, "Sign In", controller=controller, page="SignInPage", column=0, row=0, sticky="ew", bg=controller.buttonColor1, fg=controller.textColor1, columnspan=2)

    imageLinkButton(headerFrame, fileDIR=assetDIR/"settingsCog.png", size=[50,50], controller=controller, page="SettingsPage", sticky="news", column=9, row=0, columnspan=1, rowspan=1, bg=controller.headerColor1)

def drawGrids(controller, stage):
    if controller.showGrids:
        for ix in range(3):
            for iy in range(3):
                frame(
                    stage=stage,
                    column=ix, row=iy, 
                    sticky="nsew", 
                    bg="#ffffff",
                    highLightColor="black",
                    highLightWidth=1,
                )

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        self.build(parent, controller)

    def build(self, parent, controller):
        super().__init__(parent)
        self.configure(bg=controller.backgroundColor1)
        self.controller = controller
        self.columnconfigure((0, 2), weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=3)
        self.rowconfigure((1, 2), weight=5)
        
        drawGrids(controller, self)
        header(self, controller=controller)

        buttonFrame = frame(self, bg=controller.backgroundColor1, column=1, row=1, rowspan=2, sticky="nsew", rowNum=10, showGrid=controller.showGrids)
        linkButton(buttonFrame, bg=controller.buttonColor1, fg=controller.textColor1, text="Blog", page="Blog", controller=controller, column=0, row=0, sticky="news", fsize=30)
        linkButton(buttonFrame, bg=controller.buttonColor1, fg=controller.textColor1, text="Courses", page="Courses", controller=controller, column=0, row=1, sticky="news", fsize=30)
        linkButton(buttonFrame, bg=controller.buttonColor1, fg=controller.textColor1, text="Contact Us", page="ContactPage", controller=controller, column=0, row=10, sticky="news", fsize=30)

class SettingsPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.build(parent, controller)

    def setColor(self, attribute, color):
        if color != None:
            setattr(self.controller, attribute, color)
            self.controller.refresh()

    def reset(self):
        self.controller.backgroundColor1 = "#bdbdbd"
        self.controller.backgroundColor2 = "#afafaf"
        self.controller.headerColor1 = "#a0a0a0"
        self.controller.buttonColor1 = "#ffffff"
        self.controller.textColor1 = "#000000"
        self.controller.refresh()

    def build(self, parent, controller):  
        self.configure(bg=controller.backgroundColor1)
        self.controller = controller
        self.columnconfigure((0, 2), weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=3)
        self.rowconfigure((1, 2), weight=5)

        if controller.showGrids:
            for ix in range(3):
                for iy in range(3):
                    frame(
                        stage=self,
                        column=ix, row=iy, 
                        sticky="nsew", 
                        bg="#ffffff",
                        highLightColor="black",
                        highLightWidth=1,
                    )
        
        header(self, controller=controller)

        settingsFrame = frame(self, bg=controller.backgroundColor1, column=0, row=1, rowspan=2, columnspan=3, sticky="nsew", columnNum=10, rowNum=10, showGrid=controller.showGrids)
        
        tk.Checkbutton(
            settingsFrame, 
            text="Show Grids",
            variable=controller.showGridsTk,
            command=controller.toggleGrid,
            fg=controller.textColor1
        ).grid(sticky="", column=0, row=0, columnspan=1, rowspan=1)
        
        functionButton(settingsFrame, "background:", command=lambda: self.setColor('backgroundColor1', pickColor()), fg=controller.textColor1, column=0, row=1, bg=controller.buttonColor1, columnspan=2)
        frame(settingsFrame, bg=controller.backgroundColor1, column=2, row=1, sticky="nsew", highLightColor="black", highLightWidth=1, padx=10)

        functionButton(settingsFrame, "background2: ", command=lambda: self.setColor('backgroundColor2', pickColor()), fg=controller.textColor1, column=0, row=2, bg=controller.buttonColor1, columnspan=2)
        frame(settingsFrame, bg=controller.backgroundColor2, column=2, row=2, sticky="nsew", highLightColor="black", highLightWidth=1, padx=10)

        functionButton(settingsFrame, "header: ", command=lambda: self.setColor('headerColor1', pickColor()), fg=controller.textColor1, column=0, row=3, bg=controller.buttonColor1, columnspan=2)
        frame(settingsFrame, bg=controller.headerColor1, column=2, row=3, sticky="nsew", highLightColor="black", highLightWidth=1, padx=10)

        functionButton(settingsFrame, "buttons: ", command=lambda: self.setColor('buttonColor1', pickColor()), fg=controller.textColor1, column=0, row=4, bg=controller.buttonColor1, columnspan=2)
        frame(settingsFrame, bg=controller.buttonColor1, column=2, row=4, sticky="nsew", highLightColor="black", highLightWidth=1, padx=10)

        functionButton(settingsFrame, "text: ", command=lambda: self.setColor('textColor1', pickColor()), fg=controller.textColor1, column=0, row=5, bg=controller.buttonColor1, columnspan=2)
        frame(settingsFrame, bg=controller.textColor1, column=2, row=5, sticky="nsew", highLightColor="black", highLightWidth=1, padx=10)

        functionButton(settingsFrame, "RESET", command=self.reset, column=0, row=9, bg="#ffffff", columnspan=2)

class SignInPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.loginStatus = ["", controller.backgroundColor1]
        self.build(parent, controller)

    def login(self):
        userinfo = verify_login(self.user.get(), self.password.get())
        if userinfo:
            print("Login successful!")
            self.controller.loggedIn = True
            self.controller.username = userinfo["username"]
            self.controller.loggedInText = True
            col = load_colors(userinfo["username"])
            if col:
                self.controller.backgroundColor1 = col[0]
                self.controller.backgroundColor2 = col[1]
                self.controller.headerColor1 = col[2]
                self.controller.buttonColor1 = col[3]
                self.controller.textColor1 = col[4]
            self.controller.refresh()
            self.controller.show_frame("HomePage")
        else:
            self.controller.loggedInText = False
            self.controller.refresh()

    def build(self, parent, controller):
        self.configure(bg=controller.backgroundColor1)
        self.controller = controller
        self.columnconfigure((0, 2), weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=3)
        self.rowconfigure((1, 2), weight=5)
        drawGrids(controller, self)
        
        headerFrame = frame(stage=self, bg=controller.headerColor1, column=0, row=0, columnspan=3, sticky="nsew", columnNum=10, showGrid=controller.showGrids, uniform="hdr_cols")
        linkButton(headerFrame, "back", controller=controller, page="HomePage", column=0, row=0, sticky="ew", bg=controller.buttonColor1, padx=50)

        entryFrame = frame(self, bg=controller.backgroundColor1, column=1, row=1, rowspan=2, columnspan=1, sticky="nsew", columnNum=2, rowNum=10, showGrid=controller.showGrids)
        drawText(entryFrame, "Username:", bg=controller.backgroundColor1, fg=controller.textColor1, column=0, row=0, sticky="e", fsize=20, padx=10)
        self.user = tk.Entry(entryFrame, bg="#ffffff", font=("Arial", 14))
        self.user.grid(sticky="w", column=1, row=0, padx=(0,30))
        drawText(entryFrame, "Password:", bg=controller.backgroundColor1, fg=controller.textColor1, column=0, row=1, sticky="e", fsize=20, padx=10)
        self.password = tk.Entry(entryFrame, bg="#ffffff", show="*", font=("Arial", 14))
        self.password.grid(sticky="w", column=1, row=1, padx=(0,30))

        if controller.loggedInText == True:
            drawText(entryFrame, "login successful", bg=controller.backgroundColor1, fg="green", column=0, row=3, sticky="nsew", fsize=14, padx=10, columnspan=2)
        elif controller.loggedInText == False:
            drawText(entryFrame, "wrong username or password", bg=controller.backgroundColor1, fg="red", column=0, row=3, sticky="nsew", fsize=14, padx=10, columnspan=2)
        functionButton(entryFrame, "Sign In", command=self.login, column=0, row=2, columnspan=2, sticky="", bg=controller.buttonColor1)
        linkButton(entryFrame, "Sign Up", controller=controller, fg=controller.textColor1, page="SignUpPage", column=0, row=4, columnspan=2, sticky="n", bg=controller.backgroundColor1, borderwidth=0, relief="flat", bd=0, highlightthickness=0)

class SignUpPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.loginStatus = ["", controller.backgroundColor1]
        self.build(parent, controller)

    def signUp(self):
        if register_user(self.user.get(), self.password.get()) == True:
            self.controller.show_frame("SignInPage")
            save_colors(self.user.get(), 
                            [self.controller.backgroundColor1, 
                             self.controller.backgroundColor2, 
                             self.controller.headerColor1, 
                             self.controller.buttonColor1, 
                             self.controller.textColor1])
        else:
            print("Username already exists. Please choose a different username.")

    def build(self, parent, controller):  
        self.configure(bg=controller.backgroundColor1)
        self.controller = controller
        self.columnconfigure((0, 2), weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=3)
        self.rowconfigure((1, 2), weight=5)
        drawGrids(controller, self)
        
        headerFrame = frame(stage=self, bg=controller.headerColor1, column=0, row=0, columnspan=3, sticky="nsew", columnNum=10, showGrid=controller.showGrids, uniform="hdr_cols")
        linkButton(headerFrame, "back", controller=controller, page="SignInPage", column=0, row=0, sticky="ew", bg=controller.buttonColor1, padx=50)

        entryFrame = frame(self, bg=controller.backgroundColor1, column=1, row=1, rowspan=2, columnspan=1, sticky="nsew", columnNum=2, rowNum=10, showGrid=controller.showGrids)
        drawText(entryFrame, "Username:", bg=controller.backgroundColor1, fg=controller.textColor1, column=0, row=0, sticky="e", fsize=20, padx=10)
        self.user = tk.Entry(entryFrame, bg="#ffffff", font=("Arial", 14))
        self.user.grid(sticky="w", column=1, row=0, padx=(0,30))
        drawText(entryFrame, "Password:", bg=controller.backgroundColor1, fg=controller.textColor1, column=0, row=1, sticky="e", fsize=20, padx=10)
        self.password = tk.Entry(entryFrame, bg="#ffffff", show="*", font=("Arial", 14))
        self.password.grid(sticky="w", column=1, row=1, padx=(0,30))

        if controller.loggedInText == True:
            drawText(entryFrame, "login successful", bg=controller.backgroundColor1, fg="green", column=0, row=3, sticky="nsew", fsize=14, padx=10, columnspan=2)
        elif controller.loggedInText == False:
            drawText(entryFrame, "wrong username or password", bg=controller.backgroundColor1, fg="red", column=0, row=3, sticky="nsew", fsize=14, padx=10, columnspan=2)
        functionButton(entryFrame, "Sign Up", command=self.signUp, column=0, row=2, columnspan=2, sticky="", bg=controller.buttonColor1)

class Courses(tk.Frame):
    def __init__(self, parent, controller):
        self.build(parent, controller)

    def build(self, parent, controller):
        super().__init__(parent)
        self.configure(bg=controller.backgroundColor1)
        self.controller = controller
        self.columnconfigure((0, 2), weight=1, uniform="group1")
        self.columnconfigure(1, weight=2, uniform="group1")
        self.rowconfigure(0, weight=3, uniform="group1")
        self.rowconfigure((1, 2), weight=5, uniform="group1")
        drawGrids(controller, self)
        header(self, controller=controller)

        buttonsFrame = frame(self, bg=controller.backgroundColor2, column=0, row=1, rowspan=2, sticky="nsew", rowNum=10, showGrid=controller.showGrids)
    
        v_scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        pdfViewerCanvas = tk.Canvas(self, bg="gray", yscrollcommand=v_scrollbar.set, width=1, height=1)
        pdfViewerCanvas.grid(column=1, columnspan=1, row=1, rowspan=2, sticky="nesw")
        v_scrollbar.config(command=pdfViewerCanvas.yview)
        v_scrollbar.grid(sticky="nws", column=2, row=1, rowspan=2)
        functionButton(self, "← prev", bg=controller.buttonColor1, fg=controller.textColor1, command=lambda: pdf.prev_page(pdfViewerCanvas, curPageText), column=2, row=1, sticky="n", padx=(0,200))
        curPageText = drawText(self, "Page: 0 / 0", bg=controller.backgroundColor1, fg=controller.textColor1, column=2, row=1, sticky="n")
        functionButton(self, "next →", bg=controller.buttonColor1, fg=controller.textColor1, command=lambda: pdf.next_page(pdfViewerCanvas, curPageText), column=2, row=1, sticky="n", padx=(200,0))

        functionButton(buttonsFrame, "print()", sticky="nesw", command=lambda: pdf.openPdf(assetDIR/"python_print_explained.pdf", pdfViewerCanvas, curPageText), row=0)
        functionButton(buttonsFrame, "def", sticky="nesw", command=lambda: pdf.openPdf(assetDIR/"python_def_explained.pdf", pdfViewerCanvas, curPageText), row=1) 

class Blog(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.current_selected_title = None
        self.build(parent, controller)
        
    def display_post(self, title):
        self.current_selected_title = title
        post = self.controller.blogDB.get_post(title)
        
        self.postContentText.config(state="normal")
        self.postContentText.delete("1.0", tk.END)
        
        if post:
            username, title_text, content, timestamp = post
            formatted_text = f"Title: {title_text}\nAuthor: {username}\nDate: {timestamp}\n\n{content}"
            self.postContentText.insert(tk.END, formatted_text)

            # edit post button (only show if logged in and the username matches the post's author)
            if self.controller.loggedIn and self.controller.username == username:
                self.editBtn.grid(column=0, row=0, sticky="e", padx=5)
            else:
                self.editBtn.grid_forget() # use grid_forget() to hide the button if the user is not the author (better than using destroy() or refreshing page)
        else:
            self.postContentText.insert(tk.END, "Post not found.")
            self.editBtn.grid_forget()
            
        self.postContentText.config(state="disabled")

    def open_edit_page(self):
        if self.current_selected_title:
            edit_frame = self.controller.frames.get("EditPostPage")
            if edit_frame:
                edit_frame.load_post_data(self.current_selected_title)
                self.controller.show_frame("EditPostPage")

    def refresh_posts(self):
        """Clears existing buttons and rebuilds the post list from the database."""
        for child in self.selectFrame.winfo_children():
            child.destroy()

        posts = self.controller.blogDB.get_all_posts()
        for idx, i in enumerate(posts):
            functionButton(
                self.selectFrame, 
                f"{i[1]} by {i[0]}", 
                bg=self.controller.backgroundColor2, 
                fg=self.controller.textColor1, 
                column=0, 
                row=idx,
                sticky="nsew", 
                padx=10, 
                pady=5, 
                command=lambda title=i[1]: self.display_post(title)
            )

    def build(self, parent, controller):
        self.configure(bg=controller.backgroundColor1)
        self.controller = controller
        self.columnconfigure((0, 2), weight=1, uniform="group1")
        self.columnconfigure(1, weight=1, uniform="group1")
        self.rowconfigure(0, weight=3, uniform="group1")
        self.rowconfigure((1, 2), weight=5, uniform="group1")
        
        drawGrids(controller, self)
        header(self, controller=controller)
        
        blogFrame = frame(self, bg=controller.backgroundColor1, column=0, row=1, rowspan=2, columnspan=3, sticky="nsew", columnNum=10, rowNum=10, showGrid=controller.showGrids, uniform="blog_main")

        # Left sidebar for post selection (columns 0-2)
        self.selectFrame = frame(blogFrame, bg=controller.backgroundColor2, column=0, row=0, rowspan=10, columnspan=3, sticky="nsew", columnNum=1, rowNum=10, showGrid=controller.showGrids, uniform="blog_select")
        
        # Dedicated action bar container (row 0, columns 3-9)
        topBarFrame = tk.Frame(blogFrame, bg=controller.backgroundColor1)
        topBarFrame.grid(column=3, row=0, columnspan=7, sticky="nsew", padx=5, pady=5)

        # Build buttons inside the action bar container (using pack so they don't affect grid column widths)
        self.editBtn = tk.Button(
            topBarFrame, 
            text="Edit Post", 
            command=self.open_edit_page, 
            bg=controller.buttonColor1, 
            fg=controller.textColor1, 
            font=("Arial", 12),
            bd=1,
            relief="raised"
        )

        if controller.loggedIn:
            newPostBtn = tk.Button(
                topBarFrame,
                text="New Post +",
                command=lambda: controller.show_frame("NewPostPage"),
                bg=controller.buttonColor1,
                fg=controller.textColor1,
                font=("Arial", 12),
                bd=1,
                relief="raised"
            )
            newPostBtn.grid(column=1, row=0, sticky="e", padx=5)
        else:
            drawText(topBarFrame, "Sign in to post", bg=controller.backgroundColor1, fg=controller.textColor1, column=0, row=0, sticky="e", fsize=11)

        # Right area for displaying text content (row 1-9, columns 3-9)
        displayContainer = frame(blogFrame, bg=controller.backgroundColor1, column=3, row=1, rowspan=9, columnspan=7, sticky="nsew")
        displayContainer.columnconfigure(0, weight=1)
        displayContainer.rowconfigure(0, weight=1)

        self.postContentText = tk.Text(
            displayContainer, 
            bg=controller.backgroundColor1, 
            fg=controller.textColor1,
            font=("Arial", 14),
            wrap="word",
            bd=0,
            highlightthickness=0
        )
        self.postContentText.grid(column=0, row=0, sticky="nsew", padx=10, pady=10)
        self.postContentText.insert(tk.END, "Select a post to view its content:")
        self.postContentText.config(state="disabled")
        
        self.refresh_posts()


class EditPostPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.old_title = None
        self.build(parent, controller)

    def load_post_data(self, title):
        """Loads existing title and content into input fields."""
        self.old_title = title
        post = self.controller.blogDB.get_post(title)
        if post:
            _, post_title, content, _ = post
            self.titleEntry.delete(0, tk.END)
            self.titleEntry.insert(0, post_title)
            
            self.contentEntry.delete("1.0", tk.END)
            self.contentEntry.insert(tk.END, content)
            self.statusLabel.config(text="")

    def save_changes(self):
        new_title = self.titleEntry.get().strip()
        new_content = self.contentEntry.get("1.0", tk.END).strip()

        if not new_title or not new_content:
            self.statusLabel.config(text="Title and content cannot be empty.", fg="red")
            return

        try:
            self.controller.blogDB.edit_post(self.controller.username, self.old_title, new_title, new_content)
            self.controller.show_frame("Blog")
        except Exception as e:
            self.statusLabel.config(text=f"Error updating post: {e}", fg="red")

    def delete_current_post(self):
        try:
            self.controller.blogDB.delete_post(self.controller.username, self.old_title)
            self.controller.show_frame("Blog")
        except Exception as e:
            self.statusLabel.config(text=f"Error deleting post: {e}", fg="red")

    def build(self, parent, controller):
        self.configure(bg=controller.backgroundColor1)
        self.controller = controller
        self.columnconfigure((0, 2), weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=3)
        self.rowconfigure((1, 2), weight=5)

        drawGrids(controller, self)

        headerFrame = frame(stage=self, bg=controller.headerColor1, column=0, row=0, columnspan=3, sticky="nsew", columnNum=10, showGrid=controller.showGrids, uniform="hdr_cols")
        linkButton(headerFrame, "back", controller=controller, page="Blog", column=0, row=0, sticky="ew", bg=controller.buttonColor1, padx=50)

        formFrame = frame(self, bg=controller.backgroundColor1, column=1, row=1, rowspan=2, columnspan=1, sticky="nsew", columnNum=2, rowNum=10, showGrid=controller.showGrids)

        drawText(formFrame, "Edit Post", bg=controller.backgroundColor1, fg=controller.textColor1, column=0, row=0, columnspan=2, sticky="n", fsize=22, extra="bold")

        drawText(formFrame, "Title:", bg=controller.backgroundColor1, fg=controller.textColor1, column=0, row=1, columnspan=2, sticky="w", fsize=14)
        self.titleEntry = tk.Entry(formFrame, bg="#ffffff", font=("Arial", 14))
        self.titleEntry.grid(sticky="ew", column=0, row=2, columnspan=2, padx=10)

        drawText(formFrame, "Content:", bg=controller.backgroundColor1, fg=controller.textColor1, column=0, row=3, columnspan=2, sticky="w", fsize=14)
        self.contentEntry = tk.Text(formFrame, bg="#ffffff", font=("Arial", 12), wrap="word", height=6)
        self.contentEntry.grid(sticky="nsew", column=0, row=4, rowspan=3, columnspan=2, padx=10)

        self.statusLabel = drawText(formFrame, "", bg=controller.backgroundColor1, fg="red", column=0, row=7, columnspan=2, sticky="n", fsize=12)

        functionButton(formFrame, "Save Changes", command=self.save_changes, column=0, row=8, sticky="ew", bg=controller.buttonColor1, fg=controller.textColor1, fsize=12, padx=5)
        functionButton(formFrame, "Delete Post", command=self.delete_current_post, column=1, row=8, sticky="ew", bg="#ff5555", fg="white", fsize=12, padx=5)


class NewPostPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.build(parent, controller)
        
    def publish_post(self):
        title = self.titleEntry.get().strip()
        content = self.contentEntry.get("1.0", tk.END).strip()

        if not title or not content:
            self.statusLabel.config(text="Title and content cannot be empty.", fg="red")
            return

        if not self.controller.loggedIn or not self.controller.username:
            self.statusLabel.config(text="You must be logged in to post.", fg="red")
            return

        try:
            self.controller.blogDB.new_post(self.controller.username, title, content)
            self.statusLabel.config(text="Post published successfully!", fg="green")
            self.titleEntry.delete(0, tk.END)
            self.contentEntry.delete("1.0", tk.END)
            self.controller.refresh()
            self.controller.show_frame("Blog")
        except sqlite3.IntegrityError:
            self.statusLabel.config(text="A post with this title already exists.", fg="red")
        except Exception as e:
            self.statusLabel.config(text=f"Error: {e}", fg="red")

    def build(self, parent, controller):
        self.configure(bg=controller.backgroundColor1)
        self.controller = controller
        self.columnconfigure((0, 2), weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=3)
        self.rowconfigure((1, 2), weight=5)

        drawGrids(controller, self)

        headerFrame = frame(stage=self, bg=controller.headerColor1, column=0, row=0, columnspan=3, sticky="nsew", columnNum=10, showGrid=controller.showGrids, uniform="hdr_cols")
        linkButton(headerFrame, "back", controller=controller, page="Blog", column=0, row=0, sticky="ew", bg=controller.buttonColor1, padx=50)

        formFrame = frame(self, bg=controller.backgroundColor1, column=1, row=1, rowspan=2, columnspan=1, sticky="nsew", columnNum=1, rowNum=10, showGrid=controller.showGrids)

        drawText(formFrame, "Create New Post", bg=controller.backgroundColor1, fg=controller.textColor1, column=0, row=0, sticky="n", fsize=22, extra="bold")

        drawText(formFrame, "Title:", bg=controller.backgroundColor1, fg=controller.textColor1, column=0, row=1, sticky="w", fsize=14)
        self.titleEntry = tk.Entry(formFrame, bg="#ffffff", font=("Arial", 14))
        self.titleEntry.grid(sticky="ew", column=0, row=2, padx=10)

        drawText(formFrame, "Content:", bg=controller.backgroundColor1, fg=controller.textColor1, column=0, row=3, sticky="w", fsize=14)
        
        self.contentEntry = tk.Text(formFrame, bg="#ffffff", font=("Arial", 12), wrap="word", height=6)
        self.contentEntry.grid(sticky="nsew", column=0, row=4, rowspan=3, padx=10)

        self.statusLabel = drawText(formFrame, "", bg=controller.backgroundColor1, fg="red", column=0, row=7, sticky="n", fsize=12)

        functionButton(formFrame, "Publish Post", command=self.publish_post, column=0, row=8, sticky="", bg=controller.buttonColor1, fg=controller.textColor1, fsize=14)

class ContactPage(tk.Frame):
    def __init__(self, parent, controller):
        self.build(parent, controller)

    def build(self, parent, controller):
        super().__init__(parent)
        self.configure(bg=controller.backgroundColor1)
        self.controller = controller
        self.columnconfigure((0, 2), weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=3)
        self.rowconfigure((1, 2), weight=5)
        
        drawGrids(controller, self)
        header(self, controller=controller)

        drawText(self, "+61 ##########", bg=controller.backgroundColor1, fg=controller.textColor1, column=1, row=1, sticky="n", fsize=30) # currently a placeholder for a phone number (due to the nature of this being a school project, I will not be putting my real phone number here)