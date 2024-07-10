import tkinter as tk
from tkinter import ttk
import os
import sys
from PIL import Image, ImageTk

parent_dir = os.path.dirname(os.path.abspath(__file__))

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="#293C4A")
        self.create_widgets()

    def create_widgets(self):
        label = tk.Label(self, text="Smart Calculator", bg="#293C4A", fg="white", font=("Arial", 30, "bold"))
        label.grid(row=0, column=0, columnspan=2, pady=10)

        buttons = [
            ("Calculator", "Calculator_Frame", parent_dir + "\\icons\\calculator.png"),
            ("Graphing Calculator", "Graph_GUI", parent_dir + "\\icons\\graph.png"),
            ("Write to Solve", "WhiteboardApp",parent_dir + "\\icons\\write.png"),
            ("Take a Photo to Solve", "CameraApp", parent_dir + "\\icons\\photo.png"),
            ("Simultaneous Solver", "Simultaneous_solver_Frame", parent_dir + "\\icons\\simultaneous.png"),
            ("PDFReader", "PDFReader", parent_dir + "\\icons\\pdf.png"),
            ("Controls", "TransferFunctionFrame", parent_dir + "\\icons\\controls.png"),
            ("Matrix Calculator", "MatrixOperationPage", parent_dir + "\\icons\\matrix.png")
        ]

        for i, (text, frame_name, image_path) in enumerate(buttons):
            try:
                image = Image.open(image_path)
                image = image.resize((80, 80), Image.LANCZOS)
                photo = ImageTk.PhotoImage(image)

                button = tk.Button(self, text=text, image=photo, compound="top", command=lambda name=frame_name: self.controller.show_frame(name),
                                   font=("Arial", 13, "bold"), width=200, bg="#293C4A", borderwidth=0, highlightthickness=0,
                                   fg="white",pady=10)
                button.image = photo  # keep a reference to the image
                button.grid(row=(i//2) + 1, column=i % 2, pady=15, padx=10, sticky="nsew")
            except Exception as e:
                print(f"Error loading image for {text}: {e}")
                button = tk.Button(self, text=text, compound="left", command=lambda name=frame_name: self.controller.show_frame(name),
                                   font=("sans-serif", 15, "bold"), width=200, bg="white", borderwidth=2, highlightthickness=0, highlightbackground="#000000")
                button.grid(row=(i//2) + 1, column=i % 2, pady=15, padx=20, sticky="nsew")

        current_page_num_button = tk.Button(self, text="1", command=self.current_button, 
                                            font=("sans-serif", 20, "bold"), width=2, borderwidth=0, 
                                            highlightthickness=0, bg="#293C4A", fg="white", 
                                            activebackground="#293C4A", activeforeground="white")
        current_page_num_button.grid(row=6, column=0, padx=1, sticky='e')

        next_page_button = tk.Button(self, text="2", command=lambda: self.controller.show_frame("StartPage2"), 
                                     font=("sans-serif", 15, "bold"), width=2, borderwidth=0, 
                                     highlightthickness=0, bg="#293C4A", fg="white", 
                                     activebackground="#293C4A", activeforeground="white")
        next_page_button.grid(row=6, column=1, padx=1, sticky='w')


        close_button = tk.Button(self, text="Close", command=self.quit, font=("sans-serif", 15, "bold"), width=15)
        close_button.grid(row=7, column=0, columnspan=2)

        # Make the grid cells expand proportionally
        for row in range((len(buttons)//2) + 3):
            if row == 6 or row == 7:
                self.grid_rowconfigure(row)
                return
            self.grid_rowconfigure(row, weight=1)
        for col in range(2):
            self.grid_columnconfigure(col, weight=1)

    def current_button(self):
        pass

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Standalone Calculator")
    root.configure(bg="#293C4A", bd=10)
    root.geometry("400x800")
    StartPage(root, None).pack()
    root.mainloop()
