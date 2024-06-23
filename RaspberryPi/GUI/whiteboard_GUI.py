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
        self.configure(bg="#293C4A")
        self.mode = "Calculate"
        self.display_var = tk.StringVar()

        # Create widgets
        self.create_widgets()

    def create_widgets(self):
        
        self.entry = tk.Entry(self, textvariable=self.display_var, font=('sans-serif', 20, 'bold'), justify='right', state='readonly')
        self.entry.pack(fill=tk.X, ipady=30)

        self.canvas = tk.Canvas(self, bg="black", highlightthickness=0, width=10,height=600)
        self.canvas.pack(fill=tk.BOTH)

        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.reset_coords)

        button_params_main = { 'fg': '#000', 'bg': '#BBB', 'font': ('sans-serif', 15, 'bold'), 'height': 1}

        self.erase_button = tk.Button(self, text="Erase", command=self.erase, **button_params_main)
        self.erase_button.pack(side=tk.LEFT)

        self.back_button = tk.Button(self, text="Back", command=self.back, **button_params_main)
        self.back_button.pack(side=tk.LEFT)

        self.mode_button = tk.Button(self, text="Mode", command=lambda: ModeSelection_Whiteboard(self, self.set_mode), **button_params_main)
        self.mode_button.pack(side=tk.LEFT)

        self.solve_button = tk.Button(self, text=self.mode, command=self.solver, **button_params_main)
        self.solve_button.pack(side=tk.LEFT)

        self.add_button = tk.Button(self, text="Add", command=self.add, **button_params_main)
        self.add_button.pack(side=tk.LEFT)

        self.DEL_button = tk.Button(self, text="DEL", command=self.delete, **button_params_main)
        self.DEL_button.pack(side=tk.LEFT)

        self.AC_button = tk.Button(self, text="AC", command=self.clear, **button_params_main)
        self.AC_button.pack(side=tk.LEFT)

        self.previous_coords = None

    def delete(self):
        self.display_var.set(self.display_var.get()[:-1])

    def clear(self):
        self.display_var.set("")

    def set_mode(self, mode):
        self.mode = mode
        print(f"Mode set to: {mode}")
        self.update_solve_button()

    def update_solve_button(self):
        self.solve_button.config(text=self.mode)

    def draw(self, event):
        smooth_factor = 1  # Increase this value to make the lines smoother
        if self.previous_coords:
            x1, y1 = self.previous_coords
            x2, y2 = event.x, event.y
            # Interpolate between the points to create a smoother line
            steps = max(abs(x2 - x1), abs(y2 - y1)) // smooth_factor
            if steps!=0:
                for i in range(steps + 1):
                    xi = x1 + (x2 - x1) * i / steps
                    yi = y1 + (y2 - y1) * i / steps
                    self.canvas.create_line(x1, y1, xi, yi, fill="white", width=5, capstyle=tk.ROUND, smooth=True)
                    x1, y1 = xi, yi
        self.previous_coords = event.x, event.y

    def erase(self):
        self.canvas.delete("all")

    def back(self):
        self.controller.show_frame("StartPage")

    def solver(self):
        self.save_whiteboard("whiteboard/whiteboard.png")
        #answer = post_image()
        #AnswerDisplay(self, answer)
        # Add code for plotting here

    def save_whiteboard(self, filename):
        # Get the coordinates of the entire window relative to the screen
        x0 = self.winfo_rootx() + 15
        y0 = self.winfo_rooty() + 140
        x1 = x0 + 480
        y1 = y0 + 720

        # Use these coordinates to grab the screenshot and save it
        ImageGrab.grab(bbox=(x0, y0, x1, y1)).save(filename)

    def reset_coords(self, event):
        self.previous_coords = None

    def add(self):
        if not self.controller.WIFI:
            messagebox.showinfo("No Internet Connection", "Please connect to the internet to use this feature.")
            return
        
        self.save_whiteboard("whiteboard/whiteboard.png")
        self.answer = post_image()
        self.show_custom_message(self.answer)

    def show_custom_message(self, answer):
        custom_message_window = tk.Tk()
        custom_message_window.title("Processed Image")
        answer_label = tk.Label(custom_message_window, text=answer)
        answer_label.pack()
        
        add_button = tk.Button(custom_message_window, text="Add", command=lambda: self.add_action(custom_message_window))
        add_button.pack(side=tk.LEFT)
        
        retry_button = tk.Button(custom_message_window, text="Retry", command=lambda: self.retry_action(custom_message_window))
        retry_button.pack(side=tk.RIGHT)
        
        custom_message_window.mainloop()

    def add_action(self, window):
        #add answer to display
        self.display_var.set(self.display_var.get() + self.answer)
        window.destroy()

    def retry_action(self, window):
        window.destroy()
        

class ModeSelection_Whiteboard(tk.Toplevel):
    def __init__(self, parent, callback):
        super().__init__(parent)
        self.callback = callback
        self.mode_list = [
            "Calculate", "Plot", "Transfer Function", "Simultaneous Equations", "Matrix"
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
    root.geometry("300x800")
    app = WhiteboardApp(root, None)
    app.pack(fill=tk.BOTH, expand=True)
    root.mainloop()
