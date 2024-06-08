import tkinter as tk
from tkinter import ttk

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        label = tk.Label(self, text="Welcome to the Calculator App")
        label.pack(pady=10)

        calc_button = tk.Button(self, text="Calculator",
                                command=lambda: self.controller.show_frame("Calculator_Frame"))
        calc_button.pack(pady=10)

        graphing_button = tk.Button(self, text="Graphing Calculator",
                                    command=lambda: self.controller.show_frame("Graph_GUI"))
        graphing_button.pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Standalone Calculator")
    StartPage(root, None).pack()
    root.mainloop()