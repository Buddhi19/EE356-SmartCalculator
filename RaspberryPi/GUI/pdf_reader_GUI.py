import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from pdf2image import convert_from_path
import threading
import traceback
import time

class PDFReader(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.pdf_pages = []
        self.page_index = 0
        self.zoom_level = 1.0
        self.page_width = 480
        self.page_height = 800

        self.controls_frame = tk.Frame(self)
        self.controls_frame.pack(side=tk.BOTTOM, fill=tk.X)

        button_params_main = {'fg': '#000', 'bg': '#BBB', 'font': ('sans-serif', 12, 'bold')}

        self.prev_button = tk.Button(self.controls_frame, text="Previous", command=self.show_prev_page, **button_params_main)
        self.prev_button.pack(side=tk.LEFT)

        self.next_button = tk.Button(self.controls_frame, text="Next", command=self.show_next_page, **button_params_main)
        self.next_button.pack(side=tk.LEFT)

        self.zoom_in_button = tk.Button(self.controls_frame, text="Zoom In", command=self.zoom_in, **button_params_main)
        self.zoom_in_button.pack(side=tk.LEFT)

        self.zoom_out_button = tk.Button(self.controls_frame, text="Zoom Out", command=self.zoom_out, **button_params_main)
        self.zoom_out_button.pack(side=tk.LEFT)

        self.open_button = tk.Button(self.controls_frame, text="Open PDF", command=self.open_pdf, **button_params_main)
        self.open_button.pack(side=tk.RIGHT)

        self.close_button = tk.Button(self.controls_frame, text="Close PDF", command=self.close_pdf, **button_params_main)
        self.close_button.pack(side=tk.RIGHT)
        self.close_button.pack_forget()

        self.canvas = tk.Canvas(self, width=self.page_width, height=self.page_height)
        self.canvas.pack(expand=True, fill=tk.BOTH)

        self.loading_label = tk.Label(self, text="Loading PDF...", font=('sans-serif', 20))

    def open_pdf(self):
        pdf_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if pdf_path:
            print(f"Selected PDF: {pdf_path}")
            self.pdf_pages = []
            self.page_index = 0
            self.zoom_level = 1.0
            self.canvas.delete("all")
            self.loading_label.pack(expand=True)
            threading.Thread(target=self.load_pdf, args=(pdf_path,), daemon=True).start()

    def load_pdf(self, pdf_path):
        try:
            print(f"Starting PDF conversion: {pdf_path}")
            start_time = time.time()
            
            def convert_pdf():
                pages = convert_from_path(pdf_path, dpi=150, thread_count=2)
                self.pdf_pages = [self.resize_page(page) for page in pages]
            
            # Run the conversion in a separate thread with a timeout
            conversion_thread = threading.Thread(target=convert_pdf)
            conversion_thread.start()
            conversion_thread.join(timeout=30)  # Wait for 30 seconds max
            
            if conversion_thread.is_alive():
                print("PDF conversion timed out after 30 seconds")
                raise TimeoutError("PDF conversion took too long")

            end_time = time.time()
            print(f"Conversion complete. Time taken: {end_time - start_time:.2f} seconds")
            print(f"Pages converted: {len(self.pdf_pages)}")
            
            if not self.pdf_pages:
                raise ValueError("No pages were converted from the PDF.")
            
            print("Scheduling UI updates...")
            self.master.after(0, self.show_page, self.page_index)
            self.master.after(0, self.close_button.pack, {'side': tk.RIGHT})
            self.master.after(0, self.open_button.pack_forget)
            self.master.after(0, self.loading_label.pack_forget)
            print("UI updates scheduled.")
        except Exception as e:
            print(f"Error in load_pdf: {e}")
            print("Exception details:")
            traceback.print_exc()
            self.master.after(0, self.loading_label.pack_forget)
            self.master.after(0, messagebox.showerror, "Error", f"Failed to open PDF: {e}")

    def resize_page(self, page):
        return page.resize((self.page_width, self.page_height), Image.LANCZOS)

    def show_page(self, page_index):
        if self.pdf_pages:
            print(f"Showing page {page_index + 1}")
            img = self.pdf_pages[page_index]
            img = img.resize((int(self.page_width * self.zoom_level), int(self.page_height * self.zoom_level)), Image.LANCZOS)
            img_tk = ImageTk.PhotoImage(img)

            self.canvas.delete("all")
            self.canvas.config(width=self.page_width, height=self.page_height)

            x = (self.page_width - img.width) // 2
            y = (self.page_height - img.height) // 2

            self.canvas.create_image(x, y, anchor=tk.NW, image=img_tk)
            self.canvas.img_tk = img_tk
            self.master.title(f"PDF Reader - Page {page_index + 1} of {len(self.pdf_pages)}")
            print(f"Page {page_index + 1} displayed")
        else:
            print("No PDF pages to display")

    def show_prev_page(self):
        if self.pdf_pages and self.page_index > 0:
            self.page_index -= 1
            self.show_page(self.page_index)

    def show_next_page(self):
        if self.pdf_pages and self.page_index < len(self.pdf_pages) - 1:
            self.page_index += 1
            self.show_page(self.page_index)

    def zoom_in(self):
        if self.pdf_pages:
            self.zoom_level += 0.1
            self.show_page(self.page_index)

    def zoom_out(self):
        if self.pdf_pages and self.zoom_level > 0.1:
            self.zoom_level -= 0.1
            self.show_page(self.page_index)

    def close_pdf(self):
        self.pdf_pages = []
        self.canvas.delete("all")
        self.master.title("PDF Reader")
        self.close_button.pack_forget()
        self.open_button.pack(side=tk.RIGHT)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("PDF Reader")
    root.geometry("500x850")  # Adjusted to accommodate controls and match page size
    
    reader = PDFReader(root)
    reader.pack(expand=True, fill=tk.BOTH)
    
    root.mainloop()