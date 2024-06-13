import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import fitz  # PyMuPDF

class PDFReader(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        
        self.controller = controller

        self.pdf_document = None
        self.page_index = 0
        self.zoom_level = 1.0  # Initialize zoom level

        self.controls_frame = tk.Frame(self)
        self.controls_frame.pack(side=tk.BOTTOM, fill=tk.X)

        button_params_main = { 'fg': '#000', 'bg': '#BBB', 'font': ('sans-serif', 15, 'bold')}

        self.prev_button = tk.Button(self.controls_frame, text="Previous", command=self.show_prev_page,**button_params_main)
        self.prev_button.pack(side=tk.LEFT)

        self.next_button = tk.Button(self.controls_frame, text="Next", command=self.show_next_page,**button_params_main)
        self.next_button.pack(side=tk.LEFT)

        self.zoom_in_button = tk.Button(self.controls_frame, text="Zoom In", command=self.zoom_in,**button_params_main)
        self.zoom_in_button.pack(side=tk.LEFT)

        self.zoom_out_button = tk.Button(self.controls_frame, text="Zoom Out", command=self.zoom_out,**button_params_main)
        self.zoom_out_button.pack(side=tk.LEFT)

        self.open_button = tk.Button(self.controls_frame, text="Open PDF", command=self.open_pdf,**button_params_main)
        self.open_button.pack(side=tk.RIGHT)

        self.close_button = tk.Button(self.controls_frame, text="Close PDF", command=self.close_pdf,**button_params_main)
        self.close_button.pack(side=tk.RIGHT)
        self.close_button.pack_forget()  # Initially hidden

        back_button = tk.Button(self.controls_frame, text="Back", command=lambda: self.controller.show_frame("StartPage"),**button_params_main)
        back_button.pack(side=tk.RIGHT)
        
        self.canvas = tk.Canvas(self)
        self.canvas.pack(expand=True, fill=tk.BOTH)

    def open_pdf(self):
        pdf_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if pdf_path:
            try:
                self.pdf_document = fitz.open(pdf_path)
                self.page_index = 0
                self.zoom_level = 1.0  # Reset zoom level when a new PDF is opened
                self.show_page(self.page_index)
                self.close_button.pack(side=tk.RIGHT)  # Show close button when a PDF is opened
                self.open_button.pack_forget()  # Hide open button when a PDF is opened
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open PDF: {e}")

    def close_pdf(self):
        self.pdf_document = None
        self.canvas.delete("all")
        self.controller.title("PDF Reader")
        self.close_button.pack_forget()  # Hide close button when no PDF is opened
        self.open_button.pack(side=tk.RIGHT)  # Show open button when no PDF is opened

    def show_page(self, page_index):
        if self.pdf_document:
            page = self.pdf_document[page_index]
            matrix = fitz.Matrix(self.zoom_level, self.zoom_level)
            pix = page.get_pixmap(matrix=matrix)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

            img_tk = ImageTk.PhotoImage(img)

            self.canvas.delete("all")  # Clear previous images

            # Calculate the center position
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            x = (canvas_width - pix.width) // 2
            y = (canvas_height - pix.height) // 2

            self.canvas.create_image(x, y, anchor=tk.NW, image=img_tk)
            self.canvas.img_tk = img_tk
            self.controller.title(f"PDF Reader - Page {page_index + 1} of {len(self.pdf_document)}")

    def show_prev_page(self):
        if self.pdf_document and self.page_index > 0:
            self.page_index -= 1
            self.show_page(self.page_index)

    def show_next_page(self):
        if self.pdf_document and self.page_index < len(self.pdf_document) - 1:
            self.page_index += 1
            self.show_page(self.page_index)

    def zoom_in(self):
        if self.pdf_document:
            self.zoom_level += 0.1
            self.show_page(self.page_index)

    def zoom_out(self):
        if self.pdf_document and self.zoom_level > 0.1:
            self.zoom_level -= 0.1
            self.show_page(self.page_index)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("PDF Reader")
    root.geometry("330x800")
    
    reader = PDFReader(root, root)
    reader.pack(expand=True, fill=tk.BOTH)
    
    root.mainloop()
