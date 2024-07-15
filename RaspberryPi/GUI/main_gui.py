import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
from GUI.start_gui import StartPage
from GUI.start2_gui import StartPage2
from GUI.calculator_gui import Calculator_Frame
from GUI.grapher_gui import Graph_Frame2D, Graph_Frame3D, Graph_GUI
from GUI.simul_gui import Simultaneous_solver_Frame, Simultaneous_Frame
# from GUI.pdf_reader_GUI import PDFReader
from GUI.whiteboard_GUI import WhiteboardApp, ShowPlot
from GUI.controls_gui import TransferFunctionFrame, BODEplot, NyquistPlot, StepResponsePlot
from GUI.matrix_solver_gui import  MatrixOperationPage
if sys.platform == "linux":
    from GUI.cam_GUI import CameraApp
from GUI.loading_gui import Loading_GUI
from GUI.fourier_gui import FourierTransform,ShowFourierSpectrum
from GUI.laplace_gui import LaplaceTransform, ShowLaplaceTransform, ShowLaplaceSpectrum
from GUI.z_transform_GUI import DiscreteSignalCalculator
from RaspberryPi.GUI.Wifi_settings import WiFiSettingsPage
import socket

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Multiple Frames Example")
        self.attributes('-fullscreen', True)
        self.WIFI = self.is_connected()
        self.configure(bg="#293C4A")

        self.container = tk.Frame(self)
        self.container.pack(fill="both")

        self.frames = {}
        self.current_frame = None

        self.show_frame("StartPage")

    def add_frame(self, frame_class, data=None):
        frame = frame_class(self.container, self, data) if data else frame_class(self.container, self)
        self.frames[frame_class.__name__] = frame
        frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, name, data=None):
        print(f"Switching to frame: {name}")
        if self.current_frame and self.current_frame not in ["StartPage"]:
            if self.current_frame in ["Graph_Frame2D", "Graph_Frame3D","BODEplot","StepResponsePlot",
                                       "NyquistPlot","ShowFourierSpectrum","ShowLaplaceTransform","WhiteboardApp","CameraApp"]:
                if self.current_frame == "CameraApp":
                    self.frames[self.current_frame].on_hide()
                self.frames[self.current_frame].destroy()
                del self.frames[self.current_frame]
            else:
                self.frames[self.current_frame].grid_remove()

        print(f"Current Frames: {self.frames.keys()}")
        if name in self.frames:
            # Frame already exists, so just show it
            self.current_frame = name
            self.frames[name].grid()
            if name == "CameraApp":
                self.frames[name].on_show()
        else:
            # Frame doesn't exist, create it and add to frames dictionary
            frame_class = globals()[name]
            self.add_frame(frame_class, data)
            self.current_frame = name
            if name == "CameraApp":
                self.frames[name].on_show()

    def is_connected(self):
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            return True
        except OSError:
            pass
        return False    
    

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()