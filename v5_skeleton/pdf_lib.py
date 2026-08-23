import tkinter as tk

import fitz  # PyMuPDF
from PIL import Image, ImageTk


class PDFHandler:
    """Class to handle PDF operations: opening, displaying, and navigating through PDF pages."""
    def __init__(self):
        self.doc = None
        self.current_page = 0
        self.total_pages = 0
        self.img_tk = None

    def open_pdf(self, path, canv, cur_page_text):
        """Open a PDF file and display the first page on the given canvas."""
        if self.doc:
            self.doc.close()

        self.doc = fitz.open(path)
        self.current_page = 0
        self.display_page(self.current_page, canv)
        cur_page_text.config(
            text=f"Page: {self.current_page + 1} / {self.total_pages}"
        )
        canv.yview_moveto(0)

    def display_page(self, page_num, canv):
        """Display a specific page of the PDF on the given canvas."""
        if not self.doc:
            return
        canv.delete("all")

        page = self.doc.load_page(page_num)
        pix = page.get_pixmap(dpi=94)

        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        self.img_tk = ImageTk.PhotoImage(img)

        canv.create_image(0, 0, anchor=tk.NW, image=self.img_tk)
        canv.config(scrollregion=(0, 0, pix.width, pix.height))
        self.total_pages = len(self.doc)

    def next_page(self, canv, cur_page_text):
        """Navigate to the next page of the PDF and display it on the given canvas."""
        if self.doc and self.current_page < len(self.doc) - 1:
            self.current_page += 1
            self.display_page(self.current_page, canv)
            canv.yview_moveto(0)
            cur_page_text.config(
                text=f"Page: {self.current_page + 1} / {self.total_pages}"
            )

    def prev_page(self, canv, cur_page_text):
        """Navigate to the previous page of the PDF and display it on the given canvas."""
        if self.doc and self.current_page > 0:
            self.current_page -= 1
            self.display_page(self.current_page, canv)
            canv.yview_moveto(0)
            cur_page_text.config(
                text=f"Page: {self.current_page + 1} / {self.total_pages}"
            )


pdf = PDFHandler()