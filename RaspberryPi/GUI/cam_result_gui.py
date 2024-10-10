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
from whiteboard_solver import get_ans, get_transfer_function, solve_for_x


class CircularButton(tk.Canvas):
    def __init__(self, parent, width, height, color, command=None):
        super().__init__(parent, width=width, height=height, highlightthickness=0, bg="#293C4A")
        self.command = command
        self.is_pressed = False
        self.after_id = None

        # Create circle
        padding = 4
        self.create_oval(padding, padding, width-padding, height-padding, fill=color, outline="")

        self.bind("<ButtonPress-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)

    def _on_press(self, event):
        self.config(relief="sunken")
        self.is_pressed = True
        self._repeat_command()

    def _on_release(self, event):
        self.config(relief="raised")
        self.is_pressed = False
        if self.after_id:
            self.after_cancel(self.after_id)

    def _repeat_command(self):
        if self.is_pressed and self.command:
            self.command()
            self.after_id = self.after(100, self._repeat_command)


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
        self.entry = tk.Entry(self, textvariable=self.display_var, font=('Helvetica', 20, 'bold'), justify='right', state='readonly', bg="#1E2A38", fg="black", insertbackground="white")
        self.entry.grid(row=0, column=0, sticky="nsew", padx=10, pady=10, ipady=10)

        # Image display
        self.img_path = os.path.join(parent_dir, "camera", "captured_image.png")
        self.original_img = cv2.imread(self.img_path)
        self.update_image()

        control_frame = tk.Frame(self, bg="#293C4A")
        control_frame.grid(row=2, column=0, pady=10)

        # P Value Controls
        self.create_control_group(control_frame, "P value:", self.P, 0, 255, 0)

        # Iteration Controls
        self.create_control_group(control_frame, "Iterations:", self.ITERATION, 1, 20, 1)

        # Kernel Size Controls
        self.create_control_group(control_frame, "Kernel Size:", self.KERNEL_SIZE, 1, 10, 2)


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

    def create_control_group(self, parent, label_text, variable, min_val, max_val, row):
        frame = tk.Frame(parent, bg="#293C4A")
        frame.grid(row=row, column=0, pady=5, padx=5)

        tk.Label(frame, text=label_text, bg="#293C4A", fg="white", width=10, anchor="e").pack(side=tk.LEFT, padx=(0, 10))
        
        minus_btn = CircularButton(frame, 60, 60, "#FF6B6B", command=lambda: self.update_value(variable, -1, min_val, max_val))
        minus_btn.pack(side=tk.LEFT)

        value_label = tk.Label(frame, textvariable=variable, bg="#293C4A", fg="white", width=5)
        value_label.pack(side=tk.LEFT, padx=10)

        plus_btn = CircularButton(frame, 60, 60, "#4ECB71", command=lambda: self.update_value(variable, 1, min_val, max_val))
        plus_btn.pack(side=tk.LEFT)

    def update_value(self, var, change, min_val, max_val):
        new_value = var.get() + change
        if min_val <= new_value <= max_val:
            var.set(new_value)
            self.update_image()

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
        self.answer = post_image(self.save_path)
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
        elif self.current_mode == "Solve for x":
            result = solve_for_x(self.answer)
            self.display_var.set(result)


class ModeSelection_Camera(tk.Toplevel):
    def __init__(self, parent, callback):
        super().__init__(parent)
        self.callback = callback
        self.mode_list = [
            "Calculate", "Plot", "Transfer Function", "Solve for x"
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