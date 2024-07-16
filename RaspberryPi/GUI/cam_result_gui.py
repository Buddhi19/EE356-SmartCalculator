import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import sys

parent_dir = os.path.dirname(os.path.abspath(__file__))

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from cam_solver_server import post_image, get_plot_image_cam
from whiteboard_solver import get_ans, get_transfer_function

class Camera_Result_Page(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#293C4A")
        self.controller = controller
        self.current_mode = "Calculate"
        self.display_var = tk.StringVar()
        self.create_widgets()

    def create_widgets(self):
        # Configure grid
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # Entry widget
        self.entry = tk.Entry(self, textvariable=self.display_var,font=('Helvetica', 20, 'bold'), justify='right', state='readonly', bg="#1E2A38", fg="white", insertbackground="white")
        self.entry.grid(row=0, column=0, sticky="nsew", padx=10, pady=10, ipady=10)

        # Image display
        self.img_path = os.path.join(parent_dir, "camera", "captured_image.png")
        img = Image.open(self.img_path)
        img = img.resize((400, 300), Image.LANCZOS)  # Resize image
        photo = ImageTk.PhotoImage(img)
        self.image_label = tk.Label(self, image=photo, bg="#293C4A", borderwidth=0)
        self.image_label.image = photo
        self.image_label.grid(row=1, column=0, pady=10)

        # Button frame
        button_frame = tk.Frame(self, bg="#293C4A")
        button_frame.grid(row=2, column=0, pady=10)

        # Buttons
        button_style = {'bg': "#4A6572", 'fg': "white", 'font': ('Helvetica', 12), 'width': 15, 'height': 2, 'borderwidth': 0}
        
        self.back_button = tk.Button(button_frame, text="Back", command=lambda: self.controller.show_frame("CameraApp"), **button_style)
        self.back_button.grid(row=0, column=0, padx=5, pady=5)

        self.mode_button = tk.Button(button_frame, text="Select Mode", command=self.open_mode_selection, **button_style)
        self.mode_button.grid(row=0, column=1, padx=5, pady=5)

        self.process_button = tk.Button(button_frame, text="Process", command=self.process, **button_style)
        self.process_button.grid(row=1, column=0, padx=5, pady=5)

        self.solve_button = tk.Button(button_frame, text=self.current_mode, command=self.solve, **button_style)
        self.solve_button.grid(row=1, column=1, padx=5, pady=5)

    def open_mode_selection(self):
        ModeSelection_Camera(self, self.set_mode)

    def set_mode(self, mode):
        self.current_mode = mode
        print(f"Selected Mode: {self.current_mode}")
        self.update_solve_button()

    def update_solve_button(self):
        self.solve_button.config(text=self.current_mode)

    def process(self):
        self.answer = post_image(self.img_path)[0]
        print(self.answer)
        self.display_var.set(self.answer)

    def solve(self):
        # Implement this method
        print(f"Solving with mode: {self.current_mode}")
        if self.current_mode == "Plot":
            print(f"Plotting: {self.answer}")
            get_plot_image_cam(self.answer)
            self.controller.show_frame("ShowPlot_cam")
        elif self.current_mode == "Calculate":
            result = get_ans(self.answer)
            self.display_var.set(result)
        elif self.current_mode == "Transfer Function":
            ans = get_transfer_function(self.answer)
            if ans == "Error":
                self.display_var.set(ans)
            else:
                self.controller.numerator = ans[0]
                self.controller.denominator = ans[1]
                print(self.controller.numerator, self.controller.denominator)
                self.controller.show_frame("TransferFunctionFrame")


class ModeSelection_Camera(tk.Toplevel):
    def __init__(self, parent, callback):
        super().__init__(parent)
        self.callback = callback
        self.mode_list = [
            "Calculate", "Plot", "Transfer Function", "Simultaneous Equations"
        ]
        self.title("Select Mode")
        self.geometry("300x350")
        self.configure(bg="#E0E0E0")  # Light gray background
        self.create_widgets()

    def create_widgets(self):
        title_label = tk.Label(self, text="Select a Mode", font=('Helvetica', 16, 'bold'), bg="#E0E0E0", fg="#293C4A")
        title_label.pack(pady=(15, 10))

        button_style = {
            'bg': "#4A6572",
            'fg': "white",
            'font': ('Helvetica', 12),
            'width': 25,
            'height': 2,
            'borderwidth': 0,
            'activebackground': "#5A7582",
            'activeforeground': "white"
        }
        
        for mode in self.mode_list:
            button = tk.Button(self, text=mode, command=lambda m=mode: self.select_mode(m), **button_style)
            button.pack(pady=5)

    def select_mode(self, mode):
        self.callback(mode)
        self.destroy()

class ShowPlot_cam(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.image_path = "camera/plot.png"
        self.create_widgets()

    def create_widgets(self):
        self.plot_image = tk.PhotoImage(file=self.image_path)
        self.plot_label = tk.Label(self, image=self.plot_image)
        self.plot_label.pack()

        close_button = tk.Button(self, text="Close", command=lambda: self.controller.show_frame("Camera_Result_Page"))
        close_button.pack()