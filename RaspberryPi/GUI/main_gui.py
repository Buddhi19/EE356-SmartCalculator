import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
from GUI.start_gui import StartPage
from GUI.calculator_gui import Calculator_Frame
from GUI.grapher_gui import Graph_Frame2D, Graph_Frame3D, Graph_GUI
from GUI.simul_gui import Simultaneous_solver_Frame, Simultaneous_Frame
# from GUI.pdf_reader_GUI import PDFReader
from GUI.whiteboard_GUI import WhiteboardApp
from GUI.controls_gui import TransferFunctionFrame
from GUI.matrix_solver_gui import  MatrixOperationPage
from GUI.cam_GUI import CameraApp
from GUI.loading_gui import Loading_GUI

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Multiple Frames Example")
        self.geometry("330x800")
        #set full screen 
    # self.attributes('-fullscreen', True)
        # Create a menu bar
        menubar = tk.Menu(self)
        self.config(menu=menubar,bg = "#293C4A")
        

        # Initialize container to hold different frames
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)

        self.frames = {}
        self.current_frame = None

        # Add frames to the application
        self.add_frame(StartPage)
        self.add_frame(Calculator_Frame)
        self.add_frame(Graph_GUI)
        self.add_frame(Simultaneous_solver_Frame)
        # self.add_frame(PDFReader)
        self.add_frame(WhiteboardApp)
        self.add_frame(TransferFunctionFrame)
        self.add_frame(MatrixOperationPage)
        self.add_frame(CameraApp)
        self.add_frame(Loading_GUI)


        self.show_frame("StartPage")

    def add_frame(self, frame_class, data=None):
        if data:
            frame = frame_class(self.container, self, data)
        else:
            frame = frame_class(self.container, self)
        self.frames[frame_class.__name__] = frame
        frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, name, data=None):
        print(f"Switching to frame: {name}")
        if self.current_frame:
            self.frames[self.current_frame].grid_remove()
        if data:
            frame_class = globals()[name]
            frame = frame_class(self.container, self, data)
            self.frames[name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        else:
            frame_class = globals()[name]
            frame = frame_class(self.container, self)
            self.frames[name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.current_frame = name
        self.frames[name].grid()

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
