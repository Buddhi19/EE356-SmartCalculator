import os
import sys
import tkinter as tk

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import your frame classes here
from GUI.start_gui import StartPage
from GUI.calculator_gui import Calculator_Frame
from GUI.grapher_gui import Graph_GUI
from GUI.simul_gui import Simultaneous_solver_Frame
from GUI.whiteboard_GUI import WhiteboardApp
from GUI.controls_gui import TransferFunctionFrame
from GUI.matrix_solver_gui import MatrixOperationPage
if sys.platform == "linux":
    from GUI.cam_GUI import CameraApp
from GUI.loading_gui import Loading_GUI

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Multiple Frames Example")
        # self.geometry("330x800")
        #set full screen 
        self.attributes('-fullscreen', True)
        # Create a menu bar
        menubar = tk.Menu(self)
        self.config(menu=menubar,bg = "#293C4A")
        

        # Initialize container to hold different frames
        self.container = tk.Frame(self)
        self.container.pack(fill=tk.BOTH)

        self.frames = {}
        self.current_frame = None

        self.show_frame("StartPage")

    def add_frame(self, frame_class):
        frame = frame_class(self.container, self)
        self.frames[frame_class.__name__] = frame
        frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, name):
        print(f"Switching to frame: {name}")
        if self.current_frame and self.current_frame != "StartPage":
            self.frames[self.current_frame].grid_remove()
        if name not in self.frames:
            frame_class = globals()[name]
            self.add_frame(frame_class)
        self.current_frame = name
        self.frames[name].tkraise()
        self.frames[name].grid()

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
