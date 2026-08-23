import tkinter as tk
from tkinter import filedialog, messagebox
import fitz  # PyMuPDF
from PIL import Image, ImageTk

class PDFHandler():
    def __init__(self):
        self.doc = None
        self.currentPage = 0
        self.totalPages = 0
        self.img_tk = None
        

    def openPdf(self, path, canv, curPageText):
        if self.doc: # closes pdf if one is already open
            self.doc.close()

        self.doc = fitz.open(path) # opens new pdf at path
        self.currentPage = 0
        self.displayPage(self.currentPage, canv) # displates first page
        curPageText.config(text=f"Page: {self.currentPage + 1} / {self.totalPages}")
        canv.yview_moveto(0)

    def displayPage(self, pageNum, canv):
        if not self.doc: # if no pdf selected then display nothing
            return
        canv.delete("all") # wipe current canvas

        page = self.doc.load_page(pageNum) # converts the doc file into a visable image
        pix = page.get_pixmap(dpi=94)

        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        self.img_tk = ImageTk.PhotoImage(img) # converts image into ImageTk (so tkinter can use it)
    
        canv.create_image(0, 0, anchor=tk.NW, image=self.img_tk)
        canv.config(scrollregion=(0, 0, pix.width, pix.height))
        

        self.totalPages = len(self.doc)
        

    def next_page(self, canv, curPageText):
        if self.doc and self.currentPage < len(self.doc) - 1:
            self.currentPage += 1
            self.displayPage(self.currentPage, canv)
            canv.yview_moveto(0)
            curPageText.config(text=f"Page: {self.currentPage + 1} / {self.totalPages}")
            

    def prev_page(self, canv, curPageText):
        if self.doc and self.currentPage > 0:
            self.currentPage -= 1
            self.displayPage(self.currentPage, canv)
            canv.yview_moveto(0)
            curPageText.config(text=f"Page: {self.currentPage + 1} / {self.totalPages}")

pdf = PDFHandler()