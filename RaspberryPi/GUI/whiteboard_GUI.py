import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
from tkinter import messagebox
from PIL import ImageGrab
from whiteboard_solver import post_image

class WhiteboardApp(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.mode = "Calculate"
        self.create_widgets()

    def create_widgets(self):
        self.canvas = tk.Canvas(self, bg="black")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.reset_coords)

        button_params_main = { 'fg': '#000', 'bg': '#BBB', 'font': ('sans-serif', 15, 'bold')}

        self.erase_button = tk.Button(self, text="Erase", command=self.erase,**button_params_main)
        self.erase_button.pack(side=tk.LEFT)

        self.back_button = tk.Button(self, text="Back", command=self.back,**button_params_main)
        self.back_button.pack(side=tk.LEFT)

        self.mode_button = tk.Button(self, text="Mode", command=lambda: ModeSelection_Whiteboard(self, self.set_mode),**button_params_main)
        self.mode_button.pack(side=tk.LEFT)

        self.solve_button = tk.Button(self, text=self.mode, command=self.solver,**button_params_main)
        self.solve_button.pack(side=tk.RIGHT)

        self.previous_coords = None

    def set_mode(self, mode):
        self.mode = mode
        print(f"Mode set to: {mode}")
        self.update_solve_button()

    def update_solve_button(self):
        self.solve_button.config(text=self.mode)

    def draw(self, event):
        if self.previous_coords:
            x1, y1 = self.previous_coords
            x2, y2 = event.x, event.y
            self.canvas.create_line(x1, y1, x2, y2, fill="white", width=5, capstyle=tk.ROUND)
        self.previous_coords = event.x, event.y

    def erase(self):
        self.canvas.delete("all")

    def back(self):
        self.controller.show_frame("StartPage")

    def solver(self):
        self.save_whiteboard("whiteboard\\whiteboard.png")
        answer = post_image()
        AnswerDisplay(self, answer)
        # Add code for plotting here

    def save_whiteboard(self, filename):
        x0 = self.canvas.winfo_rootx() + self.canvas.winfo_x()
        y0 = self.canvas.winfo_rooty() + self.canvas.winfo_y()
        x1 = x0 + self.canvas.winfo_width()
        y1 = y0 + self.canvas.winfo_height()
        ImageGrab.grab().crop((x0, y0, x1, y1)).save(filename)

    def reset_coords(self, event):
        self.previous_coords = None

class ModeSelection_Whiteboard(tk.Toplevel):
    def __init__(self, parent, callback):
        super().__init__(parent)
        self.callback = callback
        self.mode_list = [
            "Calculate", "Plot","Transfer Function", "Simultaneous Equations", "Matrix"
        ]
        self.create_widgets()

    def create_widgets(self):
        for mode in self.mode_list:
            button = tk.Button(self, text=mode, command=lambda m=mode: self.select_mode(m))
            button.pack(fill=tk.X, pady=5)

    def select_mode(self, mode):
        self.callback(mode)
        self.destroy()

class AnswerDisplay(tk.Toplevel):
    def __init__(self, parent, answer):
        super().__init__(parent)
        self.answer = answer
        self.create_widgets()

    def create_widgets(self):
        label = tk.Label(self, text=self.answer)
        label.pack()

        close_button = tk.Button(self, text="Close", command=self.destroy)
        close_button.pack()

# Example usage:
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("330x800")
    app = WhiteboardApp(root, None)
    app.pack(fill=tk.BOTH, expand=True)
    root.mainloop()
