from NENTkintLib import *

scriptDIR = Path(__file__).resolve().parent
assetDIR = scriptDIR/"assets"


W, H = 400, 400
stage = tk.Tk()
stage.configure(bg="#999999")
stage.columnconfigure((0, 2),weight=1)
stage.columnconfigure(1,weight=1)
stage.rowconfigure(0, weight=3)
stage.rowconfigure((1, 2),weight=5)
stage.state("zoomed")


headerFrame = frame(stage, "#888888", column=0, row=0, columnspan=3, sticky="nsew", columnNum=10)

functionButton(headerFrame, "home \n[placeholder]", column=4, row=0, sticky="ew")
drawText(headerFrame, "PFP \n[placeholder]", bg="#ffffff", column=0, row=0, sticky="nsew", fsize=20)
drawText(headerFrame, "Username", bg="#888888", column=1, row=0, sticky="nsew", fsize=30)
drawText(headerFrame, "Search:", bg="#888888", column=7, row=0, sticky="e", fsize=20, padx=10)   
drawEntry(headerFrame, bg="#ffffff", column=8, padx=(0,30), sticky="w")


# buttons frame
buttonFrame = frame(stage, bg="#999999", column=1, row=1, rowspan=2, sticky="nsew", rowNum=10)
functionButton(buttonFrame, bg="#ffffff", text="Blog", column=0, row=0, sticky="news", fsize=30)
functionButton(buttonFrame, bg="#ffffff", text="Courses", column=0, row=1, sticky="news", fsize=30)
functionButton(buttonFrame, bg="#ffffff", text="Contact Us", column=0, row=10, sticky="news", fsize=30)

stage.mainloop()