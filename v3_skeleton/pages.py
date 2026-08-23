from NENTkintLib import *
from authLib import *
from pdfLib import *

scriptDIR = Path(__file__).resolve().parent
assetDIR = scriptDIR/"assets"
dbDIR = scriptDIR/"db"

def header(stage, controller):
    headerFrame = frame(stage, controller.headerColor1, column=0, row=0, columnspan=3, sticky="nsew", columnNum=10, showGrid=controller.showGrids)
    
    linkButton(headerFrame, "CODELOG", controller=controller, page="HomePage", column=3, columnspan=4, row=0, sticky="", bg=controller.headerColor1, fg=controller.textColor1, fsize=60, fstyle="Arial", extra="bold", relief="flat", bd=0, highlightthickness=0)
    if controller.loggedIn:
        drawText(headerFrame, f"Welcome, {controller.username}!", bg=controller.headerColor1, fg=controller.textColor1, column=0, row=0, sticky="", fsize=20, columnspan=3)
    else:
        linkButton(headerFrame, "Sign In", controller=controller, page="SignInPage", column=0, row=0, sticky="ew", bg=controller.buttonColor1, fg=controller.textColor1, padx=50, columnspan=2)

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
        linkButton(buttonFrame, bg=controller.buttonColor1,fg=controller.textColor1, text="Blog", page="PlaceHolderPage", controller=controller, column=0, row=0, sticky="news", fsize=30)
        linkButton(buttonFrame, bg=controller.buttonColor1,fg=controller.textColor1, text="Courses", page="Courses", controller=controller, column=0, row=1, sticky="news", fsize=30)
        linkButton(buttonFrame, bg=controller.buttonColor1,fg=controller.textColor1, text="Contact Us", page="PlaceHolderPage", controller=controller, column=0, row=10, sticky="news", fsize=30)
        

class PlaceHolderPage(tk.Frame):
    def __init__(self, parent, controller):
        self.build(parent, controller)

    def build(self, parent, controller):
        super().__init__(parent)
        self.configure(bg=controller.backgroundColor1) 
        self.columnconfigure((0,1),weight=1)
        self.rowconfigure((0,1),weight=1)
        self.controller = controller
        drawText(self, "currently a placeholder :3", bg=controller.backgroundColor1, fg=controller.textColor1, row=0, column=0, columnspan=2)   

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
        
        tk.Checkbutton( #have to do full checkbutton because controller.showGrids doesnt work in  functions unless i pass controller in (may change later)
            settingsFrame, 
            text="Show Grids",
            variable=controller.showGridsTk,
            command=controller.toggleGrid,
            fg=controller.textColor1
        ).grid(sticky="", column=0, row=0, columnspan=1, rowspan=1)
        
        functionButton(settingsFrame, "background:", command=lambda: self.setColor('backgroundColor1', pickColor()),fg=controller.textColor1, column=0, row=1, bg=controller.buttonColor1, columnspan=2)
        frame(settingsFrame, bg=controller.backgroundColor1, column=2, row=1, sticky="nsew", highLightColor="black", highLightWidth=1, padx=10)

        functionButton(settingsFrame, "background2: ", command=lambda: self.setColor('backgroundColor2', pickColor()),fg=controller.textColor1, column=0, row=2, bg=controller.buttonColor1, columnspan=2)
        frame(settingsFrame, bg=controller.backgroundColor2, column=2, row=2, sticky="nsew", highLightColor="black", highLightWidth=1, padx=10)

        functionButton(settingsFrame, "header: ", command=lambda: self.setColor('headerColor1', pickColor()),fg=controller.textColor1, column=0, row=3, bg=controller.buttonColor1, columnspan=2)
        frame(settingsFrame, bg=controller.headerColor1, column=2, row=3, sticky="nsew", highLightColor="black", highLightWidth=1, padx=10)

        functionButton(settingsFrame, "buttons: ", command=lambda: self.setColor('buttonColor1', pickColor()),fg=controller.textColor1, column=0, row=4, bg=controller.buttonColor1, columnspan=2)
        frame(settingsFrame, bg=controller.buttonColor1, column=2, row=4, sticky="nsew", highLightColor="black", highLightWidth=1, padx=10)

        functionButton(settingsFrame, "text: ", command=lambda: self.setColor('textColor1', pickColor()),fg=controller.textColor1, column=0, row=5, bg=controller.buttonColor1, columnspan=2)
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
        headerFrame = frame(stage=self, bg=controller.headerColor1, column=0, row=0, columnspan=3, sticky="nsew", columnNum=10, showGrid=controller.showGrids)
        linkButton(headerFrame, "back", controller=controller, page="HomePage", column=0, row=0, sticky="ew", bg=controller.buttonColor1, padx=50)

    
        entryFrame = frame(self, bg=controller.backgroundColor1, column=1, row=1, rowspan=2, columnspan=1, sticky="nsew", columnNum=2, rowNum=10, showGrid=controller.showGrids)
        drawText(entryFrame, "Username:", bg=controller.backgroundColor1, fg=controller.textColor1, column=0, row=0, sticky="e", fsize=20, padx=10)
        self.user = tk.Entry(entryFrame, bg="#ffffff", font=("Arial", 14))
        self.user.grid(sticky="w", column=1, row=0, padx=(0,30))
        drawText(entryFrame, "Password:", bg=controller.backgroundColor1, fg=controller.textColor1, column=0, row=1, sticky="e", fsize=20, padx=10)
        self.password = tk.Entry(entryFrame, bg="#ffffff", show="*", font=("Arial", 14))
        self.password.grid(sticky="w", column=1, row=1, padx=(0,30))
        #print(self.loginStatus)
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
        headerFrame = frame(stage=self, bg=controller.headerColor1, column=0, row=0, columnspan=3, sticky="nsew", columnNum=10, showGrid=controller.showGrids)
        linkButton(headerFrame, "back", controller=controller, page="SignInPage", column=0, row=0, sticky="ew", bg=controller.buttonColor1, padx=50)

    
        entryFrame = frame(self, bg=controller.backgroundColor1, column=1, row=1, rowspan=2, columnspan=1, sticky="nsew", columnNum=2, rowNum=10, showGrid=controller.showGrids)
        drawText(entryFrame, "Username:", bg=controller.backgroundColor1, fg=controller.textColor1, column=0, row=0, sticky="e", fsize=20, padx=10)
        self.user = tk.Entry(entryFrame, bg="#ffffff", font=("Arial", 14))
        self.user.grid(sticky="w", column=1, row=0, padx=(0,30))
        drawText(entryFrame, "Password:", bg=controller.backgroundColor1, fg=controller.textColor1, column=0, row=1, sticky="e", fsize=20, padx=10)
        self.password = tk.Entry(entryFrame, bg="#ffffff", show="*", font=("Arial", 14))
        self.password.grid(sticky="w", column=1, row=1, padx=(0,30))
        #print(self.loginStatus)
        if controller.loggedInText == True:
            drawText(entryFrame, "login successful", bg=controller.backgroundColor1, fg="green", column=0, row=3, sticky="nsew", fsize=14, padx=10, columnspan=2)
        elif controller.loggedInText == False:
            drawText(entryFrame, "wrong username or password", bg=controller.backgroundColor1, fg="red", column=0, row=3, sticky="nsew", fsize=14, padx=10, columnspan=2)
        functionButton(entryFrame, "Sign Up", command=self.signUp, column=0, row=2, columnspan=2, sticky="", bg=controller.buttonColor1)

class Courses(tk.Frame):
    def __init__(self, parent, controller):
        self.build(parent, controller)


    def build(self, parent, controller):
        super().__init__(parent) # NOTE: parent = the main frame (stage) that is being passed through the MAIN class
        self.configure(bg=controller.backgroundColor1)
        self.controller = controller # NOTE: controller = parent (in this case MAIN) used to access children of MAIN
        self.columnconfigure((0, 2),weight=1, uniform="group1")
        self.columnconfigure(1,weight=2, uniform="group1")
        self.rowconfigure(0, weight=3, uniform="group1")
        self.rowconfigure((1, 2),weight=5, uniform="group1")
        drawGrids(controller, self)
        header(self, controller=controller)

        buttonsFrame = frame(self, bg=controller.backgroundColor2, column=0, row=1, rowspan=2, sticky="nsew", rowNum=10, showGrid=controller.showGrids)
    
        v_scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        pdfViewerCanvas = tk.Canvas(self,
                    bg="gray",
                    yscrollcommand=v_scrollbar.set,
                    width=1, height=1
                )
        pdfViewerCanvas.grid(column=1, columnspan=1, row=1, rowspan=2, sticky="nesw")
        v_scrollbar.config(command=pdfViewerCanvas.yview)
        v_scrollbar.grid(sticky="nws", column=2, row=1, rowspan=2)
        functionButton(self, "← prev", bg=controller.buttonColor1, fg=controller.textColor1, command=lambda:pdf.prev_page(pdfViewerCanvas, curPageText), column=2, row=1, sticky="n", padx=(0,200))
        curPageText = drawText(self, "Page: 0 / 0", bg=controller.backgroundColor1, fg=controller.textColor1, column=2, row=1, sticky="n")
        functionButton(self, "next →", bg=controller.buttonColor1, fg=controller.textColor1, command=lambda:pdf.next_page(pdfViewerCanvas, curPageText), column=2, row=1, sticky="n", padx=(200,0))

        functionButton(buttonsFrame,"print()", sticky="nesw", command=lambda:pdf.openPdf(assetDIR/"python_print_explained.pdf", pdfViewerCanvas, curPageText), row=0)
        functionButton(buttonsFrame,"def", sticky="nesw", command=lambda:pdf.openPdf(assetDIR/"python_def_explained.pdf", pdfViewerCanvas, curPageText), row=1) 