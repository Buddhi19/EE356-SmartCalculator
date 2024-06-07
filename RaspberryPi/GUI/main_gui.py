import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
from GUI.calculator_gui import Calculator_Frame
from GUI.grapher_gui import Graph_Frame2D, Graph_Frame3D, Graph_GUI

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Multiple Frames Example")

        # Create a menu bar
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        # Create File menu with Quit option
        file_menu = tk.Menu(menubar, tearoff=False)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Quit", command=self.quit)

        # Create View menu to switch between frames
        view_menu = tk.Menu(menubar, tearoff=False)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Calculator", command=lambda: self.show_frame("Calculator_Frame"))
        view_menu.add_command(label="Grapher", command=lambda: self.show_frame("Graph_GUI"))

        # Initialize container to hold different frames
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)

        self.frames = {}
        self.current_frame = None

        # Add frames to the application
        self.add_frame(Calculator_Frame)
        self.add_frame(Graph_GUI)

        # Show the home page initially
        self.show_frame("Calculator_Frame")

    def add_frame(self, frame_class):
        frame = frame_class(self.container, self)
        self.frames[frame_class.__name__] = frame
        frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, name):
        if self.current_frame:
            self.frames[self.current_frame].grid_remove()
        self.current_frame = name
        self.frames[name].grid()

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
