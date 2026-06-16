from NENTkintLib import *

from pathlib import Path

scriptDIR = Path(__file__).resolve().parent


assetDIR = scriptDIR/"assets"


W, H = 400, 400

# WARNING! this version of the program contains many of my personal notes
# for a more proffesional and easy to read program please see other folder (NOTE: chat... make other version with less notes)
# any comment including NOTE: is a personal note and can be ignored, but it may be helpful to read it if you want to understand the code better

# HUGE DISCOVERY
# by passing tk.tk through the main class (making MAIN a child/inheriter of tk.tk) MAIN inherits all tk.tk 's functions, variables, EVERYTHING
# this can be used to define "self" as a replacement for root (for miss ws) (for sister window)

# NOTE: naming convention go brrrrr (camelCase for functions/variables and PascalCase for classes) (check at end it complies)
#color bank
backgroundColor1 = "#bdbdbd"
headerColor1 = "#a0a0a0"
buttonColor1 = "#ffffff"

showGrids = False


class MAIN(tk.Tk):
    def __init__(self, W, H):
        super().__init__()
        self.title("CodeLog")
        self.geometry(f"{W}x{H}")
        self.attributes('-zoomed', True)

        stage = tk.Frame(self)

        # NOTE: sides makes it stick to top
        # NOTE: fill makes it fill x or y (both means both)
        # NOTE: expand makes it fill screen (even if user resizes)
        stage.pack(side="top", fill="both", expand=True)

        # NOTE: weight=1 makes it fill the screen size
        stage.grid_rowconfigure(0, weight=1)
        stage.grid_columnconfigure(0, weight=1)

        # dictionary for easy access later {"dictName" : value}
        self.frames = {}


        for PageClass in (PlaceHolderPage, HomePage):
            # for each page create a new class and new frame
            page_name = PageClass.__name__ # NOTE: __name__ returns (PageTwo, PageOne) the name of the class
            frame = PageClass(parent=stage, controller=self)
            self.frames[page_name] = frame
            
            frame.grid(row=0, column=0, sticky="nsew")

    # switch to page "page_name"
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        #image(stage=self, fileDIR=assetDIR/"image.png", size=[300,200])

#NOTE: drawButton(self, "Page Three", fill=tk.X, command=lambda: controller.show_frame("PageThree"), side=tk.LEFT) # only fill x not y and stick to left wall

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent) # NOTE: parent = the main frame (stage) that is being passed through the MAIN class
        self.configure(bg=backgroundColor1)
        self.controller = controller # NOTE: controller = parent (in this case MAIN) used to access children of MAIN
        self.columnconfigure((0, 2),weight=1)
        self.columnconfigure(1,weight=1)
        self.rowconfigure(0, weight=3)
        self.rowconfigure((1, 2),weight=5)
        

        # header frame
        headerFrame = frame(self, headerColor1, column=0, row=0, columnspan=3, sticky="nsew", columnNum=10, showGrid=showGrids)
        
        drawText(headerFrame, "PFP [placeholder]", bg="#ffffff", column=0, row=0, sticky="nsew", fsize=10)
        drawText(headerFrame, "Username", bg=headerColor1, column=1, row=0, sticky="nsew", fsize=30)
        drawText(headerFrame, "Search:", bg=headerColor1, column=9, row=0, sticky="e", fsize=20, padx=10)
        drawEntry(headerFrame, bg="#ffffff", column=10, padx=(0,30), sticky="w")

        # buttons frame
        buttonFrame = frame(self, bg=backgroundColor1, column=1, row=1, rowspan=2, sticky="nsew", rowNum=10, showGrid=showGrids)
        linkButton(buttonFrame, bg=buttonColor1, text="Blog", page="PlaceHolderPage", controller=controller, column=0, row=0, sticky="news", fsize=30)
        linkButton(buttonFrame, bg=buttonColor1, text="Courses", page="PlaceHolderPage", controller=controller, column=0, row=1, sticky="news", fsize=30)
        linkButton(buttonFrame, bg=buttonColor1, text="Contact Us", page="PlaceHolderPage", controller=controller, column=0, row=10, sticky="news", fsize=30)
        variable = ""
        radioButton(buttonFrame, text="Dark Mode", variable=variable, value="dark", bg=backgroundColor1, fg="black", fstyle="Arial",  sticky="news", column=0, row=9)
        radioButton(buttonFrame, text="Light Mode", variable=variable, value="light", bg=backgroundColor1, fg="black", fstyle="Arial", sticky="news", column=0, row=8)
        

        # settings frame (placing)
        settingsFrame = frame(self, bg=backgroundColor1, column=2, row=1, rowspan=2, sticky="nsew", columnNum=4, rowNum=10, showGrid=showGrids)
        linkButton(settingsFrame, bg=buttonColor1, text="settings", page="PlaceHolderPage", controller=controller, column=4, row=10, sticky="news", fsize=30)
        
        #NOTE: Need to replace the settings text with a gear icon, but for now this will do :3
        

class PlaceHolderPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.configure(bg=backgroundColor1) 
        self.columnconfigure((0,1),weight=1)
        self.rowconfigure((0,1),weight=1)
        self.controller = controller
        drawText(self, "currently a placeholder :3", bg=backgroundColor1, row=0, column=0, columnspan=2)   

        # Buttons
        linkButton(self, "HomePage", page="HomePage", controller=controller, column=0, row=1, columnspan=2, sticky="nsew")
    


MAIN(W, H).mainloop()


