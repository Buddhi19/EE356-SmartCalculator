import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import sys
import cv2
import numpy as np

parent_dir = os.path.dirname(os.path.abspath(__file__))

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from cam_solver_server import post_image, get_plot_image_cam
from whiteboard_solver import get_ans, get_transfer_function


def DRAW_CONTOURS(img, ITERATIONS, KERNEL_SIZE):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    kernel = np.ones((KERNEL_SIZE,KERNEL_SIZE), np.uint8)
    dilated = cv2.dilate(gray, kernel, iterations=ITERATIONS)
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = [cnt for cnt in contours if (cv2.boundingRect(cnt)[2] / cv2.boundingRect(cnt)[3]) >= 0.50]
    
    if contours:
        global largest_contour
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
    
    return img, largest_contour



def PRE_PROCESS(img, P):
    img_test = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, img_test = cv2.threshold(img_test, P, 255, cv2.THRESH_BINARY)
    img_test = cv2.bitwise_not(img_test)
    return img_test

class Camera_Result_Page(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#293C4A")
        self.controller = controller
        self.current_mode = "Calculate"
        self.display_var = tk.StringVar()
        self.P = tk.IntVar(value=127)
        self.ITERATION = tk.IntVar(value=1)
        self.KERNEL_SIZE = tk.IntVar(value=1)
        self.create_widgets()

    def create_widgets(self):
        # Configure grid
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # Entry widget
        self.entry = tk.Entry(self, textvariable=self.display_var, font=('Helvetica', 20, 'bold'), justify='right', state='readonly', bg="#1E2A38", fg="white", insertbackground="white")
        self.entry.grid(row=0, column=0, sticky="nsew", padx=10, pady=10, ipady=10)

        # Image display
        self.img_path = os.path.join(parent_dir, "camera", "captured_image.png")
        self.original_img = cv2.imread(self.img_path)
        self.update_image()

        # P Slider
        slider_frame = tk.Frame(self, bg="#293C4A")
        slider_frame.grid(row=2, column=0, pady=10)
        
        slider_label = tk.Label(slider_frame, text="P value:", bg="#293C4A", fg="white")
        slider_label.pack(side=tk.LEFT, padx=(0, 50))
        
        self.p_slider = ttk.Scale(slider_frame, from_=0, to=255, orient=tk.HORIZONTAL, variable=self.P, command=self.update_image)
        self.p_slider.pack(side=tk.LEFT, expand=True, fill=tk.X)
        
        # Iteration Slider
        iteration_frame = tk.Frame(self, bg="#293C4A")
        iteration_frame.grid(row=3, column=0, pady=10)

        iteration_label = tk.Label(iteration_frame, text="Iterations:", bg="#293C4A", fg="white")
        iteration_label.pack(side=tk.LEFT, padx=(0, 50))

        self.iteration_slider = ttk.Scale(iteration_frame, from_=1, to=20, orient=tk.HORIZONTAL, variable=self.ITERATION, command=self.update_image)
        self.iteration_slider.pack(side=tk.LEFT, expand=True, fill=tk.X)

        # Kernel Size Slider
        kernel_frame = tk.Frame(self, bg="#293C4A")
        kernel_frame.grid(row=4, column=0, pady=10)

        kernel_label = tk.Label(kernel_frame, text="Kernel Size:", bg="#293C4A", fg="white")
        kernel_label.pack(side=tk.LEFT, padx=(0, 50))

        self.kernel_slider = ttk.Scale(kernel_frame, from_=1, to=10, orient=tk.HORIZONTAL, variable=self.KERNEL_SIZE, command=self.update_image)
        self.kernel_slider.pack(side=tk.LEFT, expand=True, fill=tk.X)

        # Button frame
        button_frame = tk.Frame(self, bg="#293C4A")
        button_frame.grid(row=5, column=0, pady=10)

        # Buttons
        button_style = {'bg': "#4A6572", 'fg': "white", 'font': ('Helvetica', 12), 'width': 15, 'height': 2, 'borderwidth': 0}
        
        self.back_button = tk.Button(button_frame, text="Back", command=self.go_back, **button_style)
        self.back_button.grid(row=0, column=0, padx=5, pady=5)

        self.mode_button = tk.Button(button_frame, text="Select Mode", command=self.open_mode_selection, **button_style)
        self.mode_button.grid(row=0, column=1, padx=5, pady=5)

        self.process_button = tk.Button(button_frame, text="Process", command=self.process, **button_style)
        self.process_button.grid(row=1, column=0, padx=5, pady=5)

        self.solve_button = tk.Button(button_frame, text=self.current_mode, command=self.solve, **button_style)
        self.solve_button.grid(row=1, column=1, padx=5, pady=5)

    def update_image(self, *args):
        processed_img = PRE_PROCESS(self.original_img, self.P.get())
        processed_img = cv2.cvtColor(processed_img, cv2.COLOR_GRAY2RGB)

        saving_image = processed_img.copy()
        processed_img, largest_contour = DRAW_CONTOURS(processed_img, self.ITERATION.get(), self.KERNEL_SIZE.get())

        x, y, w, h = cv2.boundingRect(largest_contour)
        saving_image = saving_image[y:y+h, x:x+w]

        processed_img = cv2.resize(processed_img, (400, 300))
        saving_image = cv2.resize(saving_image, (400, 300))

        photo = ImageTk.PhotoImage(image=Image.fromarray(processed_img))
        
        if hasattr(self, 'image_label'):
            self.image_label.configure(image=photo)
            self.image_label.image = photo
        else:
            self.image_label = tk.Label(self, image=photo, bg="#293C4A", borderwidth=0)
            self.image_label.image = photo
            self.image_label.grid(row=1, column=0, pady=10)
        
        self.save_path = os.path.join(parent_dir, "camera", "processed_image.png")
        cv2.imwrite(self.save_path, saving_image)

    def go_back(self):
        if sys.platform == "linux":
            self.controller.show_frame("CameraApp")
        else:
            self.controller.show_frame("StartPage")

    def open_mode_selection(self):
        ModeSelection_Camera(self, self.set_mode)

    def set_mode(self, mode):
        self.current_mode = mode
        print(f"Selected Mode: {self.current_mode}")
        self.update_solve_button()

    def update_solve_button(self):
        self.solve_button.config(text=self.current_mode)

    def process(self):
        self.answer = post_image(self.save_path)[0]
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
        self.image_path = os.path.join(parent_dir, "camera", "plot.png")
        self.create_widgets()

    def create_widgets(self):
        self.plot_image = tk.PhotoImage(file=self.image_path)
        self.plot_label = tk.Label(self, image=self.plot_image)
        self.plot_label.pack()

        close_button = tk.Button(self, text="Close", command=lambda: self.controller.show_frame("Camera_Result_Page"))
        close_button.pack()