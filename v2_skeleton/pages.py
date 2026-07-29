from NENTkintLib import *
from authLib import *

scriptDIR = Path(__file__).resolve().parent
assetDIR = scriptDIR/"assets"
dbDIR = scriptDIR/"db"

def header(stage, controller):
    headerFrame = frame(stage, controller.headerColor1, column=0, row=0, columnspan=3, sticky="nsew", columnNum=10, showGrid=controller.showGrids)
    linkButton(headerFrame, "home \n[placeholder]", controller=controller, page="HomePage", column=4, row=0, sticky="ew", bg=controller.buttonColor1)
    if controller.loggedIn:
        drawText(headerFrame, f"Welcome, {controller.username}!", bg=controller.headerColor1, column=0, row=0, sticky="nsew", fsize=20, columnspan=3, padx=10)
    else:
        linkButton(headerFrame, "Sign In", controller=controller, page="SignInPage", column=0, row=0, sticky="ew", bg=controller.buttonColor1, padx=50, columnspan=2)

    drawText(headerFrame, "Search:", bg=controller.headerColor1, column=7, row=0, sticky="e", fsize=20, padx=10)   
    drawEntry(headerFrame, bg="#ffffff", column=8, padx=(0,30), sticky="w")
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
        super().__init__(parent) # NOTE: parent = the main frame (stage) that is being passed through the MAIN class
        self.configure(bg=controller.backgroundColor1)
        self.controller = controller # NOTE: controller = parent (in this case MAIN) used to access children of MAIN
        self.columnconfigure((0, 2),weight=1)
        self.columnconfigure(1,weight=1)
        self.rowconfigure(0, weight=3)
        self.rowconfigure((1, 2),weight=5)
        
        drawGrids(controller, self)
        

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
        linkButton(self, "HomePage", page="HomePage", controller=controller, column=0, row=1, columnspan=2, sticky="nsew", bg=controller.buttonColor1)
    

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
        self.controller.headerColor1 = "#a0a0a0"
        self.controller.buttonColor1 = "#ffffff"
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
        
        tk.Checkbutton( #have to do full checkbutton because controller.showGrids doesnt work in  functions unless i pass controller in (may change later)
            settingsFrame, 
            text="Show Grids",
            variable=controller.showGridsTk,
            command=controller.toggleGrid
        ).grid(sticky="", column=0, row=0, columnspan=1, rowspan=1)
        
        functionButton(settingsFrame, "background:", command=lambda: self.setColor('backgroundColor1', pickColor()), column=0, row=1, bg=controller.buttonColor1, columnspan=2)
        frame(settingsFrame, bg=controller.backgroundColor1, column=2, row=1, sticky="nsew", highLightColor="black", highLightWidth=1, padx=10)

        functionButton(settingsFrame, "header: ", command=lambda: self.setColor('headerColor1', pickColor()), column=0, row=2, bg=controller.buttonColor1, columnspan=2)
        frame(settingsFrame, bg=controller.headerColor1, column=2, row=2, sticky="nsew", highLightColor="black", highLightWidth=1, padx=10)

        functionButton(settingsFrame, "buttons: ", command=lambda: self.setColor('buttonColor1', pickColor()), column=0, row=3, bg=controller.buttonColor1, columnspan=2)
        frame(settingsFrame, bg=controller.buttonColor1, column=2, row=3, sticky="nsew", highLightColor="black", highLightWidth=1, padx=10)

        functionButton(settingsFrame, "RESET", command=self.reset, column=0, row=9, bg="#ffffff", columnspan=2)


class SignInPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.build(parent, controller)

    def login(self):
        userinfo = verify_login(self.user.get(), self.password.get())
        if userinfo:
            print("Login successful!")
            self.controller.loggedIn = True
            self.controller.username = userinfo["username"]
            self.controller.refresh()
        else:
            print("Login failed. Invalid username or password.")

    def build(self, parent, controller):  
        self.configure(bg=controller.backgroundColor1)
        self.controller = controller
        self.columnconfigure((0, 2), weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=3)
        self.rowconfigure((1, 2), weight=5)
        drawGrids(controller, self)
        headerFrame = frame(stage=self, bg=controller.headerColor1, column=0, row=0, columnspan=3, sticky="nsew", columnNum=10, showGrid=controller.showGrids)
        linkButton(headerFrame, "home \n[placeholder]", controller=controller, page="HomePage", column=4, row=0, sticky="ew", bg=controller.buttonColor1)

    
        entryFrame = frame(self, bg=controller.backgroundColor1, column=1, row=1, rowspan=2, columnspan=1, sticky="nsew", columnNum=2, rowNum=10, showGrid=controller.showGrids)
        drawText(entryFrame, "Username:", bg=controller.backgroundColor1, column=0, row=0, sticky="e", fsize=20, padx=10)
        self.user = tk.Entry(entryFrame, bg="#ffffff", font=("Arial", 14))
        self.user.grid(sticky="w", column=1, row=0, padx=(0,30))
        drawText(entryFrame, "Password:", bg=controller.backgroundColor1, column=0, row=1, sticky="e", fsize=20, padx=10)
        self.password = tk.Entry(entryFrame, bg="#ffffff", show="*", font=("Arial", 14))
        self.password.grid(sticky="w", column=1, row=1, padx=(0,30))

        functionButton(entryFrame, "Sign In", command=self.login, column=0, row=2, columnspan=2, sticky="nsew", bg=controller.buttonColor1)

        
