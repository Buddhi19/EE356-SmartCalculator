import tkinter as tk
from tkinter import ttk

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Multi-Frame Calculator App")
        self.geometry("400x300")

        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        self.frames = {}

        for F in (StartPage, CalculatorPage, GraphingCalculatorPage, Graph2DPage, Graph3DPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        label = tk.Label(self, text="Welcome to the Calculator App")
        label.pack(pady=10)

        calc_button = tk.Button(self, text="Calculator",
                                command=lambda: self.controller.show_frame("CalculatorPage"))
        calc_button.pack(pady=10)

        graphing_button = tk.Button(self, text="Graphing Calculator",
                                    command=lambda: self.controller.show_frame("GraphingCalculatorPage"))
        graphing_button.pack(pady=10)

class CalculatorPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        label = tk.Label(self, text="Calculator Page")
        label.pack(pady=10)

        back_button = tk.Button(self, text="Back to Main Menu",
                                command=lambda: self.controller.show_frame("StartPage"))
        back_button.pack(pady=10)

class GraphingCalculatorPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        label = tk.Label(self, text="Graphing Calculator Page")
        label.pack(pady=10)

        graph_2d_button = tk.Button(self, text="2D Graph",
                                    command=lambda: self.controller.show_frame("Graph2DPage"))
        graph_2d_button.pack(pady=10)

        graph_3d_button = tk.Button(self, text="3D Graph",
                                    command=lambda: self.controller.show_frame("Graph3DPage"))
        graph_3d_button.pack(pady=10)

        back_button = tk.Button(self, text="Back to Main Menu",
                                command=lambda: self.controller.show_frame("StartPage"))
        back_button.pack(pady=10)

class Graph2DPage(tk.Frame):
    def __init__(self, parent, controller, data=None):
        super().__init__(parent)
        self.controller = controller
        self.data = data
        self.create_widgets()

    def create_widgets(self):
        label = tk.Label(self, text="2D Graph Page")
        label.pack(pady=10)

        back_button = tk.Button(self, text="Back to Graphing Calculator",
                                command=lambda: self.controller.show_frame("GraphingCalculatorPage"))
        back_button.pack(pady=10)

class Graph3DPage(tk.Frame):
    def __init__(self, parent, controller, data=None):
        super().__init__(parent)
        self.controller = controller
        self.data = data
        self.create_widgets()

    def create_widgets(self):
        label = tk.Label(self, text="3D Graph Page")
        label.pack(pady=10)

        back_button = tk.Button(self, text="Back to Graphing Calculator",
                                command=lambda: self.controller.show_frame("GraphingCalculatorPage"))
        back_button.pack(pady=10)

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
