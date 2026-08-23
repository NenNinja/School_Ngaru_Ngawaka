from pages import *

W, H = 400, 400

def on_closing():
    # Save the colors to the database before closing
    if main.loggedIn and main.username:
        save_colors(main.username,
                    [main.backgroundColor1, 
                    main.backgroundColor2, 
                    main.headerColor1, 
                    main.buttonColor1, 
                    main.textColor1])
    close_connection()  # Close the database connection
    main.blogDB.close_connection()
    main.destroy()

class MAIN(tk.Tk):
    """
    MAIN
    scaffold frame for other frames to be placed upon, (replacement for root)
    """

    def __init__(self, W, H):
        super().__init__()
        # THESE ARE NOT CONSTANTS, they are just default values, they can be changed in the settings page or when a user logs in and has their own colors saved in the database
        self.backgroundColor1 = "#bdbdbd"
        self.backgroundColor2 = "#afafaf"
        self.headerColor1 = "#a0a0a0"
        self.buttonColor1 = "#ffffff"
        self.textColor1 = "#000000"
        self.loggedInText = None
        self.loggedIn = False
        self.username = None
        get_connection(dbDIR/"userInformation.db")  # Establish database connection
        setup_db()
        self.blogDB = BlogDB(dbDIR/"userInformation.db")
        self.blogDB.setup_db()

        self.currentPage = None
        self.title("CodeLog")
        self.geometry(f"{W}x{H}")
        self.state('zoomed')

        self.showGrids = False
        self.showGridsTk = tk.BooleanVar(value=self.showGrids)

        self.stage = tk.Frame(self)
        self.stage.pack(side="top", fill="both", expand=True)
        self.stage.grid_rowconfigure(0, weight=1, uniform="group1")
        self.stage.grid_columnconfigure(0, weight=1, uniform="group1")

        # dictionary for easy access later {"dictName" : value}
        self.frames = {}
        self.buildAllFrames(self.stage)

    def buildAllFrames(self, stage):
        """Build all the frames for the application. uses classes from pages.py"""
        for PageClass in (Courses, SignUpPage, SignInPage, Blog, EditPostPage, NewPostPage, ContactPage, SettingsPage, HomePage):
            # print(PageClass.__name__)
            # for each page create a new class and new frame
            page_name = PageClass.__name__ # NOTE: __name__ returns the name of the class {>>>("name")<<< : "value"}
            frame = PageClass(parent=stage, controller=self)
            self.frames[page_name] = frame
            
            frame.grid(row=0, column=0, sticky="nsew")

    # switch to page "page_name"
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        
        # If navigating to the Blog frame, fetch latest posts from the database
        if page_name == "Blog" and hasattr(frame, "refresh_posts"):
            frame.refresh_posts()
            
        frame.tkraise()
        self.currentPage = page_name

    def refresh(self):
        for frame in self.frames.values():
            frame.destroy()  # Destroy the existing frame
        self.frames = {}
        self.buildAllFrames(self.stage)
        self.show_frame(self.currentPage)
        
    def setattribute(self, attribute, value):
        setattr(self, attribute, value)
        self.refresh()
    
    def toggleGrid(self):
        self.showGrids = self.showGridsTk.get()
        self.refresh()
  



main = MAIN(W, H)


main.protocol("WM_DELETE_WINDOW", on_closing)
main.mainloop()