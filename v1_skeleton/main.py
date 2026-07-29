from NENTkintLib import *

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



class MAIN(tk.Tk):
    """
    MAIN
    scaffold frame for other frames to be placed upon, (replacement for root)
    """

    def __init__(self, W, H):
        super().__init__()
        self.backgroundColor1 = "#bdbdbd"
        self.headerColor1 = "#a0a0a0"
        self.buttonColor1 = "#ffffff"
        self.currentPage = None
        self.title("CodeLog")
        self.geometry(f"{W}x{H}")
        self.state('zoomed') 
        self.configure(bg="#ff0000")

        self.showGrids = False
        self.showGridsTk = tk.BooleanVar(value=self.showGrids)

        self.stage = tk.Frame(self)

        # NOTE: sides makes it stick to top
        # NOTE: fill makes it fill x or y (both means both)
        # NOTE: expand makes it fill screen (even if user resizes)
        self.stage.pack(side="top", fill="both", expand=True)

        # NOTE: weight=1 makes it fill the screen size
        self.stage.grid_rowconfigure(0, weight=1)
        self.stage.grid_columnconfigure(0, weight=1)

        # dictionary for easy access later {"dictName" : value}
        self.frames = {}
        self.buildAllFrames(self.stage)

    def buildAllFrames(self, stage):
        for PageClass in (PlaceHolderPage, SettingsPage, HomePage):
            print(PageClass.__name__)
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
        #image(stage=self, fileDIR=assetDIR/"image.png", size=[300,200])

    
    def refresh(self):
        for frame in self.frames.values():
            frame.destroy()
        self.frames = {}
        self.buildAllFrames(self.stage)
        self.show_frame(self.currentPage)
        
        
        print(self.frames)

    def setattribute(self, attribute, value):
        setattr(self, attribute, value)
        self.refresh()
    
    def toggleGrid(self):
        print("toggled grid")
        self.showGrids = self.showGridsTk.get()
        self.refresh()

#NOTE: drawButton(self, "Page Three", fill=tk.X, command=lambda: controller.show_frame("PageThree"), side=tk.LEFT) # only fill x not y and stick to left wall


def header(stage, controller):
    headerFrame = frame(stage, controller.headerColor1, column=0, row=0, columnspan=3, sticky="nsew", columnNum=10, showGrid=controller.showGrids)

    linkButton(headerFrame, "home \n[placeholder]", controller=controller, page="HomePage", column=4, row=0, sticky="ew")
    drawText(headerFrame, "PFP \n[placeholder]", bg="#ffffff", column=0, row=0, sticky="nsew", fsize=20)
    drawText(headerFrame, "Username", bg=controller.headerColor1, column=1, row=0, sticky="nsew", fsize=30)
    drawText(headerFrame, "Search:", bg=controller.headerColor1, column=7, row=0, sticky="e", fsize=20, padx=10)   
    drawEntry(headerFrame, bg="#ffffff", column=8, padx=(0,30), sticky="w")
    imageLinkButton(headerFrame, fileDIR=assetDIR/"settingsCog.png", size=[50,50], controller=controller, page="SettingsPage", sticky="news", column=9, row=0, columnspan=1, rowspan=1, bg=controller.headerColor1)
    

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        self.build(parent, controller)


    def build(self, parent, controller):
        super().__init__(parent) # NOTE: parent = the main frame (stage) that is being passed through the MAIN class
        self.configure(bg=controller.backgroundColor1)
        self.controller = controller # NOTE: controller = parent (in this case MAIN) used to access children of MAIN
        self.columnconfigure((0, 2),weight=1)
        self.columnconfigure(1,weight=1)
        self.rowconfigure(0, weight=3)
        self.rowconfigure((1, 2),weight=5)
        
        if controller.showGrids == True:
            for ix in range(3):
                for iy in range(3):
                    frame(
                        stage=self,
                        column=ix, row=iy, 
                        sticky="nsew", 
                        bg="#ffffff",
                        highLightColor="black",   # This sets the border color
                        highLightWidth=1,        # This sets the border width in pixels
                        )
        

        # header frame
        header(self, controller=controller)

        # buttons frame
        buttonFrame = frame(self, bg=controller.backgroundColor1, column=1, row=1, rowspan=2, sticky="nsew", rowNum=10, showGrid=controller.showGrids)
        linkButton(buttonFrame, bg=controller.buttonColor1, text="Blog", page="PlaceHolderPage", controller=controller, column=0, row=0, sticky="news", fsize=30)
        linkButton(buttonFrame, bg=controller.buttonColor1, text="Courses", page="PlaceHolderPage", controller=controller, column=0, row=1, sticky="news", fsize=30)
        linkButton(buttonFrame, bg=controller.buttonColor1, text="Contact Us", page="PlaceHolderPage", controller=controller, column=0, row=10, sticky="news", fsize=30)
        
        #variable = ""
        #radioButton(buttonFrame, text="Dark Mode", variable=variable, value="dark", bg=controller.backgroundColor1, fg="black", fstyle="Arial",  sticky="news", column=0, row=9)
        #radioButton(buttonFrame, text="Light Mode", variable=variable, value="light", bg=controller.backgroundColor1, fg="black", fstyle="Arial", sticky="news", column=0, row=8)
        

        # settings frame (placing)
        settingsFrame = frame(self, bg=controller.backgroundColor1, column=2, row=1, rowspan=2, sticky="nsew", columnNum=6, rowNum=10, showGrid=controller.showGrids)
        
        
        
        #DAN WAS HERE

class PlaceHolderPage(tk.Frame):
    def __init__(self, parent, controller):
        self.build(parent, controller)

    def build(self, parent, controller):
        super().__init__(parent)
        self.configure(bg=controller.backgroundColor1) 
        self.columnconfigure((0,1),weight=1)
        self.rowconfigure((0,1),weight=1)
        self.controller = controller
        drawText(self, "currently a placeholder :3", bg=controller.backgroundColor1, row=0, column=0, columnspan=2)   

        # Buttons
        linkButton(self, "HomePage", page="HomePage", controller=controller, column=0, row=1, columnspan=2, sticky="nsew")
    

class SettingsPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.build(parent, controller)

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

        settingsFrame = frame(self, bg=controller.backgroundColor1, column=0, row=1, rowspan=2, columnspan=3, sticky="nsew", columnNum=5, rowNum=10, showGrid=controller.showGrids)
        
        tk.Checkbutton( #have to do full checkbutton because controller.showGrids doesnt work in  functions unless i pass controller in (may change later)
            settingsFrame, 
            text="Show Grids",
            variable=controller.showGridsTk,
            command=controller.toggleGrid
        ).grid(sticky="", column=0, row=0, columnspan=1, rowspan=1)
        
        functionButton(settingsFrame, "change bg1 col", command=lambda: controller.setattribute('backgroundColor1', pickColor()), column=0, row=1)
        frame(settingsFrame, bg=controller.backgroundColor1, column=0, row=2, sticky="nsew", bd=1, highLightColor="black", highLightWidth=1)
        

main = MAIN(W, H)
main.mainloop()