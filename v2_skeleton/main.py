from pages import *

W, H = 400, 400



# WARNING! this version of the program contains many of my personal notes
# for a more proffesional and easy to read program please see other folder (NOTE: chat... make other version with less notes)
# any comment including NOTE: is a personal note and can be ignored, but it may be helpful to read it if you want to understand the code better

# NOTE: HUGE DISCOVERY
# by passing tk.Tk through the main class (making MAIN a child/inheriter of tk.Tk) MAIN inherits all tk.Tk 's functions, variables, EVERYTHING
# this can be used to define "self" as a replacement for root (for miss ws) (for sister window)

# NOTE: naming convention (camelCase for functions/variables and PascalCase for classes) (check at end it complies)

def on_closing():
    close_connection()  # Close the database connection
    main.destroy()

    with open(scriptDIR / "config.txt", "r") as file: # read the config file and update it with the current colors
        lines = file.read().splitlines()
        lines[0] = lines[0].split("=")[0] + "=" + main.backgroundColor1
        lines[1] = lines[1].split("=")[0] + "=" + main.headerColor1
        lines[2] = lines[2].split("=")[0] + "=" + main.buttonColor1

    with open(scriptDIR / "config.txt", "w") as file:
        for line in lines:
            file.write(line + "\n")

class MAIN(tk.Tk):
    """
    MAIN
    scaffold frame for other frames to be placed upon, (replacement for root)
    """

    def __init__(self, W, H):
        super().__init__()

        with open(scriptDIR/"config.txt", "r") as file:
            content = []
            for i in file.read().splitlines():
                content.append(i.split("=")[1])
            print(content)

        self.backgroundColor1 = content[0]
        self.headerColor1 = content[1]
        self.buttonColor1 = content[2]
        self.loggedIn = False
        self.username = None
        get_connection(dbDIR/"userInformation.db")  # Establish database connection
        setup_db()

        self.currentPage = None
        self.title("CodeLog")
        self.geometry(f"{W}x{H}")
        self.state('zoomed') 
        self.configure(bg="#ff0000")

        self.showGrids = False
        self.showGridsTk = tk.BooleanVar(value=self.showGrids)

        self.stage = tk.Frame(self)
        self.stage.pack(side="top", fill="both", expand=True)
        self.stage.grid_rowconfigure(0, weight=1)
        self.stage.grid_columnconfigure(0, weight=1)

        # dictionary for easy access later {"dictName" : value}
        self.frames = {}
        self.buildAllFrames(self.stage)


    def buildAllFrames(self, stage):
        for PageClass in (SignInPage, PlaceHolderPage, SettingsPage, HomePage):
            # print(PageClass.__name__)
            # for each page create a new class and new frame
            page_name = PageClass.__name__ # NOTE: __name__ returns the name of the class {>>>("name")<<< : "value"}
            frame = PageClass(parent=stage, controller=self)
            self.frames[page_name] = frame
            
            frame.grid(row=0, column=0, sticky="nsew") 

    # switch to page "page_name"
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        self.currentPage = page_name

    
    def refresh(self):
        for frame in self.frames.values():
            frame.destroy()
        self.frames = {}
        self.buildAllFrames(self.stage)
        self.show_frame(self.currentPage)
        
        
        # print(self.frames)

    def setattribute(self, attribute, value):
        setattr(self, attribute, value)
        self.refresh()
    
    def toggleGrid(self):
        # print("toggled grid")
        self.showGrids = self.showGridsTk.get()
        self.refresh()
  



main = MAIN(W, H)


main.protocol("WM_DELETE_WINDOW", on_closing)
main.mainloop()