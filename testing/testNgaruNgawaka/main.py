from NENTkintLib import *
W, H = 450, 550

scriptDIR = Path(__file__).resolve().parent
assetDIR = scriptDIR/"assets"

class MAIN(tk.Tk):
    def __init__(self, W, H):
        super().__init__()
        self.title("check")
        self.geometry(f"{W}x{H}")

        stage = tk.Frame(self)
        stage.pack(side="top", fill="both", expand=True)

        stage.config(height=5)
        stage.grid_rowconfigure((0, 1, 2, 3, 4), weight=2)
        stage.grid_columnconfigure(0, weight=1)
        stage.propagate(False)

        header = frame(stage, "#003A70", 0, 0, sticky="nesw")

        drawText(header, "MACLEANS\nCOLLEGE", column=0, row=0, bg="#003A70", fg="#C9A227", fstyle="Times New Roman", fsize=22, extra="bold")
        image(header, assetDIR/"Macleans_College_logo.png", [100,100], sticky="w")

        mainF = frame(stage, column=0, row=1, rowspan=2, sticky="nsew", padx=10, pady=10, bg="#ffffff", bd=1)
        drawText(mainF, "Name:", sticky="nw", padx=5, pady=(20,0), fg="#003A70", fstyle="Times New Roman")
        drawText(mainF, "Date:", sticky="nw", padx=5, pady=(60,0), fg="#003A70", fstyle="Times New Roman")
        drawText(mainF, "Time:", sticky="nw", padx=5, pady=(100,0), fg="#003A70", fstyle="Times New Roman")
        drawText(mainF, "House:", sticky="nw", padx=5, pady=(140,0), fg="#003A70", fstyle="Times New Roman")
        drawEntry(mainF, sticky="nw", padx=80, pady=(20,0), fg="#003A70", fstyle="Times New Roman")
        drawEntry(mainF, sticky="nw", padx=80, pady=(60,0), fg="#003A70", fstyle="Times New Roman")
        drawEntry(mainF, sticky="nw", padx=80, pady=(100,0), fg="#003A70", fstyle="Times New Roman")
        drawEntry(mainF, sticky="nw", padx=80, pady=(140,0), fg="#003A70", fstyle="Times New Roman")
        
        
        extra = frame(stage, bg="#003A70", row=4, sticky="nesw", padx=20, pady=20, bd=2)
        drawText(extra, "Excellence is not an act, but a habit.", bg="#003A70", fg="#C9A227", fstyle="Times New Roman", extra="italic", sticky="n", pady=20)
        functionButton(extra, "↻ New Quote", fg="#003A70", fstyle="Times New Roman", bg="#C9A227", sticky="s", pady=10)
    

MAIN(W, H).mainloop()