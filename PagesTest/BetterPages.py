from NENTkintLib import *

W, H = 400, 400

# WARNING! this version of the program contains many of my personal notes
# for a more proffesional and easy to read program please see other folder (NOTE TO SELF, chat... make other version with less notes)

# HUGE DISCOVERY
# by passing tk.tk through the main class (making MAIN a child/inheriter of tk.tk) MAIN inherits all tk.tk 's functions, variables, EVERYTHING
# this can be used to define "self" as a replacement for root (for miss ws) (for sister window)

class MAIN(tk.Tk):
    def __init__(self, W, H):
        super().__init__()
        self.title("check")
        self.geometry(f"{W}x{H}")

        stage = tk.Frame(self)

        # sides makes it stick to top
        # fill makes it fill x or y (both means both)
        # expand makes it fill screen (even if user resizes)
        stage.pack(side="top", fill="both", expand=True)

        # weight=1 makes it fill the screen size
        stage.grid_rowconfigure(0, weight=1)
        stage.grid_columnconfigure(0, weight=1)

        # dictionary for easy access later
        self.frames = {}

        for PageClass in (PageTwo, PageThree, PageOne):
            # for each page create a new class
            page_name = PageClass.__name__
            frame = PageClass(parent=stage, controller=self)
            self.frames[page_name] = frame
            
            frame.grid(row=0, column=0, sticky="nsew")

    # switch to page "page_name"
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


#drawButton(self, "Page Three", fill=tk.X, command=lambda: controller.show_frame("PageThree"), side=tk.LEFT) # only fill x not y and stick to left wall

class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent) # parent = parents self (dont judge im dumb)
        self.controller = controller # controller = parent (in this case MAIN) used to access children of MAIN
        drawText(self, "Page 1", bg='#5d8a82', padx=20, pady=20, expand=True, fill=tk.BOTH)
        
        # Buttons
        linkButton(self, "Previous Page", expand=True, fill=tk.BOTH, side=tk.LEFT, page="PageThree", controller=controller, pady=5)
        linkButton(self, "Next Page", expand=True, fill=tk.BOTH, side=tk.RIGHT, page="PageTwo", controller=controller, pady=5)

class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        drawText(self, "Page 2", bg='#ffbf00', padx=20, pady=20, expand=True, fill=tk.BOTH)
        
        # Buttons
        linkButton(self, "Previous Page", expand=True, fill=tk.BOTH, side=tk.LEFT, page="PageOne", controller=controller, pady=5)
        linkButton(self, "Next Page", expand=True, fill=tk.BOTH, side=tk.RIGHT, page="PageThree", controller=controller, pady=5)

class PageThree(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        drawText(self, "Page 3", bg="#bb00ff", padx=20, pady=20, expand=True, fill=tk.BOTH)
        
        # Buttons
        linkButton(self, "Previous Page", expand=True, fill=tk.BOTH, side=tk.LEFT, page="PageTwo", controller=controller, pady=5)
        linkButton(self, "Next Page", expand=True, fill=tk.BOTH, side=tk.RIGHT, page="PageOne", controller=controller, pady=5)

MAIN(W, H).mainloop()
