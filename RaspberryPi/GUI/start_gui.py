import tkinter as tk
from tkinter import ttk
import os
import sys
from PIL import Image, ImageTk

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="#293C4A")
        self.create_widgets()

    def create_widgets(self):
        label = tk.Label(self, text="Smart Calculator", bg="#293C4A", fg="#BBB", font=("Arial", 20, "bold"))
        label.grid(row=0, column=0, columnspan=2)

        buttons = [
            ("Calculator", "Calculator_Frame"),
            ("Graphing Calculator", "Graph_GUI"),
            ("Write to Solve", "WhiteboardApp"),
            ("Take a Photo to Solve", "TakePhotoToSolve"),
            ("Simultaneous Solver", "Simultaneous_solver_Frame"),
            ("PDFReader", "PDFReader"),
            ("Controls", "TransferFunctionFrame"),
            ("Matrix Calculator", "MatrixOperationPage")
        ]

        for i, (text, frame_name) in enumerate(buttons):
            button = tk.Button(self, text=text, command=lambda name=frame_name: self.controller.show_frame(name),
                               font=("sans-serif", 15, "bold"),width=20)
            #center the buttons
            button.grid(row=i+1,pady=5,padx=45)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Standalone Calculator")
    root.configure(bg="#293C4A", bd=10)
    root.geometry("330x800")
    StartPage(root, None).pack()
    root.mainloop()