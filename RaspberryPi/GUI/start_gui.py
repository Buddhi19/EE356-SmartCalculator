import tkinter as tk
from tkinter import ttk

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="#293C4A")
        self.create_widgets()

    def create_widgets(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(9, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        label = tk.Label(self, text="Smart Calculator", bg="#293C4A", fg="#BBB", font=("sans-serif", 20, "bold"))
        label.grid(row=0, column=0, pady=10)

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
                               font=("sans-serif", 15, "bold"),width=25)
            button.grid(row=i+1, column=0, pady=5,padx=0, sticky='ew')

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Standalone Calculator")
    root.configure(bg="#293C4A", bd=10)
    root.geometry("330x800")
    StartPage(root, None).pack()
    root.mainloop()