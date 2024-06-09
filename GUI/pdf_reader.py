import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import fitz  # PyMuPDF

class PDFReader(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("PDF Reader")
        self.geometry("400x800")

        self.pdf_document = None
        self.page_index = 0

        self.controls_frame = tk.Frame(self)
        self.controls_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.prev_button = tk.Button(self.controls_frame, text="Previous", command=self.show_prev_page)
        self.prev_button.pack(side=tk.LEFT)

        self.next_button = tk.Button(self.controls_frame, text="Next", command=self.show_next_page)
        self.next_button.pack(side=tk.LEFT)

        self.open_button = tk.Button(self.controls_frame, text="Open PDF", command=self.open_pdf)
        self.open_button.pack(side=tk.RIGHT)

        self.close_button = tk.Button(self.controls_frame, text="Close PDF", command=self.close_pdf)
        self.close_button.pack(side=tk.RIGHT)
        self.close_button.pack_forget()  # Initially hidden

        self.canvas = tk.Canvas(self, bg="grey", width=400, height=750)
        self.canvas.pack(side=tk.TOP, expand=tk.YES, fill=tk.BOTH)

    def open_pdf(self):
        pdf_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if pdf_path:
            try:
                self.pdf_document = fitz.open(pdf_path)
                self.page_index = 0
                self.show_page(self.page_index)
                self.close_button.pack(side=tk.RIGHT)  # Show close button when a PDF is opened
                self.open_button.pack_forget()  # Hide open button when a PDF is opened
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open PDF: {e}")

    def close_pdf(self):
        self.pdf_document = None
        self.canvas.delete("all")
        self.title("PDF Reader")
        self.close_button.pack_forget()  # Hide close button when no PDF is opened
        self.open_button.pack(side=tk.RIGHT)  # Show open button when no PDF is opened

    def show_page(self, page_index):
        if self.pdf_document:
            page = self.pdf_document[page_index]
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            
            # Resize the image to fit within 400x750 while maintaining the aspect ratio
            max_width, max_height = 400, 700  # Reduced max_height to fit buttons
            img_ratio = img.width / img.height
            target_ratio = max_width / max_height

            if img_ratio > target_ratio:
                # Image is wider relative to its height
                new_width = max_width
                new_height = int(max_width / img_ratio)
            else:
                # Image is taller relative to its width
                new_width = int(max_height * img_ratio)
                new_height = max_height

            img = img.resize((new_width, new_height), Image.LANCZOS)
            img_tk = ImageTk.PhotoImage(img)

            self.canvas.delete("all")  # Clear previous images

            # Calculate the center position
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            x = (canvas_width - new_width) // 2
            y = (canvas_height - new_height) // 2

            self.canvas.create_image(x, y, anchor=tk.NW, image=img_tk)
            self.canvas.img_tk = img_tk
            self.title(f"PDF Reader - Page {page_index + 1} of {len(self.pdf_document)}")

    def show_prev_page(self):
        if self.pdf_document and self.page_index > 0:
            self.page_index -= 1
            self.show_page(self.page_index)

    def show_next_page(self):
        if self.pdf_document and self.page_index < len(self.pdf_document) - 1:
            self.page_index += 1
            self.show_page(self.page_index)

if __name__ == "__main__":
    app = PDFReader()
    app.mainloop()
