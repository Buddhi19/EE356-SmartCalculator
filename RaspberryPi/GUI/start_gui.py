import tkinter as tk
from tkinter import ttk

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="#293C4A")
        self.create_widgets()

    def create_widgets(self):
        label = tk.Label(self, text="Welcome to the Calculator App", bg="#293C4A", fg="#BBB", font=("sans-serif", 20, "bold"))
        label.pack(pady=10)

        calc_button = tk.Button(self, text="Calculator",
                                command=lambda: self.controller.show_frame("Calculator_Frame"), font=("sans-serif", 15, "bold"))
        calc_button.pack(pady=10)

        graphing_button = tk.Button(self, text="Graphing Calculator",
                                    command=lambda: self.controller.show_frame("Graph_GUI"),font=("sans-serif", 15, "bold"))
        graphing_button.pack(pady=10)

        write_to_solve = tk.Button(self, text="Write to Solve",
                                    command=lambda: self.controller.show_frame("WhiteboardApp"))
        write_to_solve.pack(pady=10)

        take_a_photo_to_solve = tk.Button(self, text="Take a Photo to Solve",
                                        command=lambda: self.controller.show_frame("TakePhotoToSolve"),font=("sans-serif", 15, "bold"))
        take_a_photo_to_solve.pack(pady=10)

        simultaneous_solver = tk.Button(self, text="Simultaneous Solver",
                                        command=lambda: self.controller.show_frame("Simultaneous_solver_Frame"),font=("sans-serif", 15, "bold"))
        simultaneous_solver.pack(pady=10)

        ebook = tk.Button(self, text="Pdf Reader",
                                        command=lambda: self.controller.show_frame("Ebook"),font=("sans-serif", 15, "bold"))
        ebook.pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Standalone Calculator")
    root.configure(bg="#293C4A", bd=10)
    root.geometry("480x800")
    StartPage(root, None).pack()
    root.mainloop()