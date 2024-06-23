import tkinter as tk
from tkinter import ttk
import os
import sys
from PIL import Image, ImageTk


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
            ("Calculator", "Calculator_Frame", "icons/calculator.png"),
            ("Graphing Calculator", "Graph_GUI", "icons/graph.png"),
            ("Write to Solve", "WhiteboardApp", "icons/write.png"),
            ("Take a Photo to Solve", "TakePhotoToSolve", "icons/photo.png"),
            ("Simultaneous Solver", "Simultaneous_solver_Frame", "icons/simultaneous.png"),
            ("PDFReader", "PDFReader", "icons/pdf.png"),
            ("Controls", "TransferFunctionFrame", "icons/controls.png"),
            ("Matrix Calculator", "MatrixOperationPage", "icons/matrix.png")
        ]

        for i, (text, frame_name, image_path) in enumerate(buttons):
            try:
                image = Image.open(image_path)
                image = image.resize((80, 80), Image.LANCZOS)
                photo = ImageTk.PhotoImage(image)

                button = tk.Button(self, text=text, image=photo, compound="top", command=lambda name=frame_name: self.controller.show_frame(name),
                                   font=("Arial", 13, "bold"), width=180, bg="#293C4A", borderwidth=0, highlightthickness=0,
                                   fg="white",pady=10)
                button.image = photo  # keep a reference to the image
                button.grid(row=(i//2) + 1, column=i % 2, pady=15, padx=10, sticky="nsew")
            except Exception as e:
                print(f"Error loading image for {text}: {e}")
                button = tk.Button(self, text=text, compound="left", command=lambda name=frame_name: self.controller.show_frame(name),
                                   font=("sans-serif", 15, "bold"), width=200, bg="white", borderwidth=2, highlightthickness=0, highlightbackground="#000000")
                button.grid(row=(i//2) + 1, column=i % 2, pady=15, padx=20, sticky="nsew")

        close_button = tk.Button(self, text="Close", command=self.quit, font=("sans-serif", 15, "bold"), width=20)
        close_button.grid(row=(len(buttons)//2) + 2, column=0, columnspan=2, pady=20)

        # Make the grid cells expand proportionally
        for row in range((len(buttons)//2) + 3):
            self.grid_rowconfigure(row, weight=1)
        for col in range(2):
            self.grid_columnconfigure(col, weight=1)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Standalone Calculator")
    root.configure(bg="#293C4A", bd=10)
    root.geometry("400x800")
    StartPage(root, None).pack()
    root.mainloop()
