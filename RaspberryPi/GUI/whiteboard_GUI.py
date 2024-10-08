import os
import sys

parent_dir = os.path.dirname(os.path.abspath(__file__))

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
from tkinter import messagebox
from PIL import ImageGrab
from whiteboard_solver import post_image, get_ans, get_plot_image, get_transfer_function, solve_for_x

class WhiteboardApp(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="#293C4A")
        self.mode = "Calculate"
        self.display_var = tk.StringVar()
        self.cell_size = 110
        self.grid_visible = True
        self.is_erasing = False  # Flag to track eraser mode

        # Create widgets
        self.create_widgets()

    def create_widgets(self):
        self.entry = tk.Entry(self, textvariable=self.display_var, font=('sans-serif', 20, 'bold'), justify='right', state='readonly')
        self.entry.grid(row=0, column=0, columnspan=4, ipady=30, sticky="nsew")

        self.canvas = tk.Canvas(self, bg="black", highlightthickness=0, width=480, height=600)
        self.canvas.grid(row=1, column=0, columnspan=4, sticky="nsew")

        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.reset_coords)

        button_params_main = {'fg': '#000', 'bg': '#BBB', 'font': ('sans-serif', 10, 'bold'), 'height': 1}
        
        self.clear_button = tk.Button(self, text="Clear", command=self.clear, **button_params_main)
        self.clear_button.grid(row=2, column=0, sticky="nsew")

        self.back_button = tk.Button(self, text="Back", command=self.back, **button_params_main)
        self.back_button.grid(row=3, column=2, sticky="nsew")

        self.erase_button = tk.Button(self, text="Erase", command=self.erase, **button_params_main)
        self.erase_button.grid(row=3, column=0, sticky="nsew")

        self.mode_button = tk.Button(self, text="Mode", command=lambda: ModeSelection_Whiteboard(self, self.set_mode), **button_params_main)
        self.mode_button.grid(row=3, column=1, sticky="nsew")

        self.solve_button = tk.Button(self, text=self.mode, command=self.solver, **button_params_main)
        self.solve_button.grid(row=3, column=3, sticky="nsew")

        self.add_button = tk.Button(self, text="Process", command=self.add, **button_params_main)
        self.add_button.grid(row=2, column=1, sticky="nsew")

        self.DEL_button = tk.Button(self, text="DEL", command=self.delete, **button_params_main)
        self.DEL_button.grid(row=2, column=2, sticky="nsew")

        self.AC_button = tk.Button(self, text="AC", command=self.delete_all, **button_params_main)
        self.AC_button.grid(row=2, column=3, sticky="nsew")

        self.previous_coords = None

        # Configure grid weights to make the widgets resize proportionally
        for i in range(7):
            self.columnconfigure(i, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=0)

        self.draw_grid()

    def draw_grid(self):
        if self.grid_visible:
            width = int(self.canvas.cget("width"))
            height = int(self.canvas.cget("height"))
            for i in range(0, width, self.cell_size):
                self.canvas.create_line([(i, 0), (i, height)], tag='grid_line', fill='gray')
            for i in range(0, height, self.cell_size):
                self.canvas.create_line([(0, i), (width, i)], tag='grid_line', fill='gray')

    def clear_grid(self):
        self.canvas.delete('grid_line')

    def delete(self):
        self.display_var.set(self.display_var.get()[:-1])

    def delete_all(self):
        self.display_var.set("")

    def clear(self):
        self.canvas.delete("all")
        if self.grid_visible:
            self.draw_grid()

    def set_mode(self, mode):
        self.mode = mode
        print(f"Mode set to: {mode}")
        self.update_solve_button()

    def update_solve_button(self):
        self.solve_button.config(text=self.mode)

    def draw(self, event):
        smooth_factor = 1  # Increase this value to make the lines smoother
        color = "black" if self.is_erasing else "white"
        if self.previous_coords:
            x1, y1 = self.previous_coords
            x2, y2 = event.x, event.y
            # Interpolate between the points to create a smoother line
            steps = max(abs(x2 - x1), abs(y2 - y1)) // smooth_factor
            if steps!=0:
                for i in range(steps + 1):
                    xi = x1 + (x2 - x1) * i / steps
                    yi = y1 + (y2 - y1) * i / steps
                    self.canvas.create_line(x1, y1, xi, yi, fill=color, width=5, capstyle=tk.ROUND, smooth=True)
                    x1, y1 = xi, yi
        self.previous_coords = event.x, event.y

        if self.is_erasing:
            self.draw_grid()

    def erase(self):
        self.is_erasing = not self.is_erasing
        self.erase_button.config(relief=tk.SUNKEN if self.is_erasing else tk.RAISED)

    def back(self):
        self.controller.show_frame("StartPage")

    def solver(self):
        self.save_whiteboard(os.path.join(parent_dir, "whiteboard", "whiteboard.png"))
        #answer = post_image()
        #AnswerDisplay(self, answer)
        # Add code for plotting here

    def save_whiteboard(self, filename):
        # Get the coordinates of the entire window relative to the screen
        x0 = self.winfo_rootx() + 15
        y0 = self.winfo_rooty() + 140
        x1 = x0 + 480
        y1 = y0 + 560

        # Use these coordinates to grab the screenshot and save it
        ImageGrab.grab(bbox=(x0, y0, x1, y1)).save(filename)

    def reset_coords(self, event):
        self.previous_coords = None

    def add(self):
        if not self.controller.WIFI:
            messagebox.showinfo("No Internet Connection", "Please connect to the internet to use this feature.")
            return
        
        self.save_whiteboard(os.path.join(parent_dir,"whiteboard", "whiteboard.png"))
        self.answer = post_image()
        self.show_custom_message(self.answer)

    def show_custom_message(self, answer):
        custom_message_window = tk.Tk()
        custom_message_window.title("Processed Image")
        answer_label = tk.Label(custom_message_window, text=answer)
        answer_label.pack()
        
        add_button = tk.Button(custom_message_window, text="Solve", command=lambda: self.add_action(custom_message_window))
        add_button.pack(side=tk.LEFT)
        
        retry_button = tk.Button(custom_message_window, text="Retry", command=lambda: self.retry_action(custom_message_window))
        retry_button.pack(side=tk.RIGHT)
        
        custom_message_window.mainloop()

    def add_action(self, window):
        #add answer to display
        if self.mode == "Calculate":
            if "x" in self.answer:
                self.answer = self.answer.replace("x", r"\times")
            if "X" in self.answer:
                self.answer = self.answer.replace("X", r"\times")
            ans = get_ans(self.answer)
            self.display_var.set(ans)
            window.destroy()
        if self.mode == "Plot":
            if "X" in self.answer:
                self.answer.replace("X", "x")
            if "Y" in self.answer:
                self.answer.replace("Y", "y")
            if "Z" in self.answer:
                self.answer.replace("Z", "z")
            if get_plot_image(self.answer) == 1:
                window.destroy()
                self.controller.show_frame("ShowPlot")
            else:
                window.destroy()
                messagebox.showinfo("Error", "Failed to generate plot image.")
        if self.mode == "Transfer Function":
            ans = get_transfer_function(self.answer)
            if ans == "Error":
                self.display_var.set(ans)
            else:
                self.controller.numerator = ans[0]
                self.controller.denominator = ans[1]
                print(self.controller.numerator, self.controller.denominator)
                window.destroy()
                self.controller.show_frame("TransferFunctionFrame")
        if self.mode == "Solve for x":
            ans = solve_for_x(self.answer)
            if type(ans) == list:
                ans = ", ".join(ans)
            self.display_var.set(ans)
            window.destroy()



    def retry_action(self, window):
        window.destroy()

class ModeSelection_Whiteboard(tk.Toplevel):
    def __init__(self, parent, callback):
        super().__init__(parent, bg="#293C4A")
        self.callback = callback
        self.mode_list = [
            "Calculate", "Plot", "Transfer Function", "Solve for x"
        ]
        self.create_widgets()

    def create_widgets(self):
        button_params_main = {'fg': '#000', 'bg': '#BBB', 'font': ('sans-serif', 10, 'bold')}
        for mode in self.mode_list:
            button = tk.Button(self, text=mode, command=lambda m=mode: self.select_mode(m),**button_params_main)
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

class ShowPlot(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.image_path = os.path.join(parent_dir,"whiteboard", "plot.png")
        self.create_widgets()

    def create_widgets(self):
        self.plot_image = tk.PhotoImage(file=self.image_path)
        self.plot_label = tk.Label(self, image=self.plot_image)
        self.plot_label.pack()

        close_button = tk.Button(self, text="Close", command=lambda: self.controller.show_frame("WhiteboardApp"))
        close_button.pack()

# Example usage:
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("300x800")
    app = WhiteboardApp(root, None)
    app.pack(fill=tk.BOTH, expand=True)
    root.mainloop()
