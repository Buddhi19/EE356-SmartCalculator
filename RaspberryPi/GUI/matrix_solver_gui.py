import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

#from main_controller import Calculator
import tkinter as tk
from tkinter import ttk
import numpy as np
from matrix_solver import MatrixSolver
import math
from PIL import ImageGrab
class MatrixInputPage(tk.Toplevel):
    def __init__(self, parent, callback):
        super().__init__(parent)
        self.callback = callback
        self.configure(bg="#293C4A")

        label = tk.Label(self, text="Enter Matrix Dimensions", font=('sans-serif', 24, 'bold'), bg="#293C4A", fg="#BBB")
        label.pack(pady=20)

        self.row_var = tk.IntVar(value=2)
        self.col_var = tk.IntVar(value=2)

        row_label = tk.Label(self, text="Rows:", font=('sans-serif', 15, 'bold'), bg="#293C4A", fg="#BBB")
        row_label.pack(pady=5)
        self.row_menu = ttk.Combobox(self, textvariable=self.row_var, values=[2, 3, 4, 5,6], font=('sans-serif', 15, 'bold'))
        self.row_menu.pack(pady=5)

        col_label = tk.Label(self, text="Columns:", font=('sans-serif', 15, 'bold'), bg="#293C4A", fg="#BBB")
        col_label.pack(pady=5)
        self.col_menu = ttk.Combobox(self, textvariable=self.col_var, values=[2, 3, 4, 5,6], font=('sans-serif', 15, 'bold'))
        self.col_menu.pack(pady=5)

        self.matrix_var = tk.StringVar(value='MatA')
        matrix_label = tk.Label(self, text="Select Matrix:", font=('sans-serif', 15, 'bold'), bg="#293C4A", fg="#BBB")
        matrix_label.pack(pady=5)
        self.matrix_menu = ttk.Combobox(self, textvariable=self.matrix_var, values=['MatA', 'MatB', 'MatC', 'MatD', 'MatE','MatF'], font=('sans-serif', 15, 'bold'))
        self.matrix_menu.pack(pady=5)

        button = tk.Button(self, text="Next", command=self.next_page,
                           font=('sans-serif', 15, 'bold'), bg="#BBB", fg="#000")
        button.pack(pady=20)

        write_button = tk.Button(self, text="Write and add", command=self.on_write_click, font=('sans-serif', 15, 'bold'), bg="#BBB", fg="#000")
        write_button.pack(pady=10)

    def on_write_click(self):
        Whiteboard(self)

    def next_page(self):
        rows = self.row_var.get()
        cols = self.col_var.get()
        matrix_name = self.matrix_var.get()
        self.callback(rows, cols, matrix_name)
        self.destroy()

class Whiteboard(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(bg="#293C4A")
        self.title("Whiteboard")
        self.geometry("480x800")
        self.mode = "Calculate"
        self.display_var = tk.StringVar()
        self.cell_size = 130
        self.grid_visible = True

        # Create widgets
        self.create_widgets()

    def create_widgets(self):
        self.canvas = tk.Canvas(self, bg="black", highlightthickness=0, width=480, height=600)
        self.canvas.grid(row=1, column=0, columnspan=4, sticky="nsew")

        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.reset_coords)

        button_params_main = {'fg': '#000', 'bg': '#BBB', 'font': ('sans-serif', 10, 'bold'), 'height': 1}
        
        self.erase_button = tk.Button(self, text="Erase", command=self.erase, **button_params_main)
        self.erase_button.grid(row=2, column=0, sticky="nsew")

        self.back_button = tk.Button(self, text="Back", command=self.back, **button_params_main)
        self.back_button.grid(row=3, column=0, sticky="nsew")

        self.mode_button = tk.Button(self, text="Mode", command=lambda: ModeSelection_Whiteboard(self, self.set_mode), **button_params_main)
        self.mode_button.grid(row=3, column=1, sticky="nsew")

        self.solve_button = tk.Button(self, text=self.mode, command=self.solver, **button_params_main)
        self.solve_button.grid(row=3, column=2,columnspan=2, sticky="nsew")

        self.add_button = tk.Button(self, text="Add", command=self.add, **button_params_main)
        self.add_button.grid(row=2, column=1, sticky="nsew")

        self.DEL_button = tk.Button(self, text="DEL", command=self.delete, **button_params_main)
        self.DEL_button.grid(row=2, column=2, sticky="nsew")

        self.AC_button = tk.Button(self, text="AC", command=self.clear, **button_params_main)
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
            if steps != 0:
                for i in range(steps + 1):
                    xi = x1 + (x2 - x1) * i / steps
                    yi = y1 + (y2 - y1) * i / steps
                    self.canvas.create_line(x1, y1, xi, yi, fill="white", width=5, capstyle=tk.ROUND, smooth=True)
                    x1, y1 = xi, yi
        self.previous_coords = event.x, event.y

    def erase(self):
        self.canvas.delete("all")
        if self.grid_visible:
            self.draw_grid()

    def back(self):
        self.destroy()

    def solver(self):
        self.save_whiteboard("whiteboard.png")
        # Add solver logic here

    def save_whiteboard(self, filename):
        # Get the coordinates of the entire window relative to the screen
        x0 = self.winfo_rootx() + 15
        y0 = self.winfo_rooty() + 140
        x1 = x0 + 480
        y1 = y0 + 580

        # Use these coordinates to grab the screenshot and save it
        ImageGrab.grab(bbox=(x0, y0, x1, y1)).save(filename)

    def reset_coords(self, event):
        self.previous_coords = None

    def add(self):
        self.save_whiteboard("whiteboard.png")
        # Add logic to process and add content here

class ModeSelection_Whiteboard(tk.Toplevel):
    def __init__(self, parent, callback):
        super().__init__(parent, bg="#293C4A")
        self.callback = callback
        self.mode_list = [
            "Calculate", "Plot", "Transfer Function", "Simultaneous Equations", "Matrix"
        ]
        self.create_widgets()

    def create_widgets(self):
        button_params_main = {'fg': '#000', 'bg': '#BBB', 'font': ('sans-serif', 10, 'bold')}
        for mode in self.mode_list:
            button = tk.Button(self, text=mode, command=lambda m=mode: self.select_mode(m), **button_params_main)
            button.pack(fill=tk.X, pady=5)

    def select_mode(self, mode):
        self.callback(mode)
        self.destroy()

class MatrixEntryPage(tk.Toplevel):
    def __init__(self, parent, callback):
        super().__init__(parent)
        self.callback = callback
        self.configure(bg="#293C4A")

        self.label = tk.Label(self, text="Enter Matrix Values", font=('sans-serif', 24, 'bold'), bg="#293C4A", fg="#BBB")
        self.label.pack(pady=20)

        self.matrix_frame = tk.Frame(self, bg="#293C4A")
        self.matrix_frame.pack()

        self.num_pad_frame = tk.Frame(self, bg="#293C4A")
        self.num_pad_frame.pack()

        self.num_pad = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2),
            ('0', 4, 1), ('.', 4, 0), ('-', 4, 2)
        ]

        self.entries = []

        for (text, row, col) in self.num_pad:
            button = tk.Button(self.num_pad_frame, text=text, command=lambda t=text: self.num_pad_click(t),
                               font=('sans-serif', 15, 'bold'), bg="#BBB", fg="#000", width=5)
            button.grid(row=row, column=col)

        self.current_entry = None

        self.add_button = tk.Button(self, text="Add Matrix", command=self.add_matrix,
                                    font=('sans-serif', 15, 'bold'), bg="#BBB", fg="#000")
        self.add_button.pack(pady=20)

        back_button = tk.Button(self, text="Back", command=lambda: self.destroy(),
                                font=('sans-serif', 15, 'bold'), bg="#BBB", fg="#000")
        back_button.pack(pady=10)

    def set_matrix_details(self, rows, cols, matrix_name):
        self.rows = rows
        self.cols = cols
        self.matrix_name = matrix_name
        self.create_matrix_entries()

    def create_matrix_entries(self):
        for widget in self.matrix_frame.winfo_children():
            widget.destroy()
        self.entries = []

        for r in range(self.rows):
            row_entries = []
            for c in range(self.cols):
                entry = tk.Entry(self.matrix_frame, font=('sans-serif', 15, 'bold'), width=5)
                entry.grid(row=r, column=c, padx=5, pady=5)
                entry.bind("<FocusIn>", self.set_current_entry)
                row_entries.append(entry)
            self.entries.append(row_entries)

    def set_current_entry(self, event):
        self.current_entry = event.widget

    def num_pad_click(self, value):
        if self.current_entry is not None:
            current_text = self.current_entry.get()
            if value == 'DEL':
                self.current_entry.delete(len(current_text) - 1)
            elif value == 'CLR':
                self.current_entry.delete(0, tk.END)
            else:
                self.current_entry.insert(tk.END, value)

    def add_matrix(self):
        matrix = []
        for row_entries in self.entries:
            row = [float(entry.get()) for entry in row_entries]
            matrix.append(row)
            print(row)
        self.callback(self.matrix_name, matrix)
        self.destroy()

class MatrixOperationPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.display_var = tk.StringVar()
        self.configure(bg="#293C4A")
        self.create_widgets()

        self.matrices = {name: None for name in ['MatA', 'MatB', 'MatC', 'MatD', 'MatE', 'MatF']}
        self.solver = MatrixSolver(self.matrices['MatA'], self.matrices['MatB'], self.matrices['MatC'], self.matrices['MatD'], self.matrices['MatE'], self.matrices['MatF'])

        self.label = tk.Label(self, text="Matrix Operations", font=('sans-serif', 20, 'bold'), bg="#293C4A", fg="#BBB")
        self.label.grid(row=0, column=0, columnspan=3, pady=20, padx=10)

        self.operation_entry = tk.Entry(self, textvariable=self.display_var, font=('sans-serif', 15, 'bold'), bg="#BBB", fg="#000", justify='right', width=30)
        self.operation_entry.grid(row=1, column=0, columnspan=3, pady=10,padx=10)

        self.result_label = tk.Label(self, text="", font=('sans-serif', 15, 'bold'), bg="white", fg="#BBB", width=30)
        self.result_label.grid(row=2, column=0, columnspan=3, pady=10)

        self.operation_pad_frame = tk.Frame(self, bg="#293C4A")
        self.operation_pad_frame.grid(row=3, column=0, columnspan=3, pady=10,padx=(50,15))

    def create_widgets(self):
        self.button_params = {'fg': '#BBB', 'bg': '#3C3636', 'font': ('sans-serif', 11, 'bold')}
        self.button_params_main = {'fg': '#000', 'bg': '#BBB', 'font': ('sans-serif', 11, 'bold')}
        self.button_params_other = {'fg': '#000', 'bg': '#db701f', 'font': ('sans-serif', 11, 'bold')}

        row1_buttons = ['←', '→', 'pi']
        row2_buttons = ['+', '-', '*']
        row3_buttons = ['7', '8', '9']
        row4_buttons = ['4', '5', '6']
        row5_buttons = ['1', '2', '3']
        row6_buttons = ['0', '.', 'inv']
        row7_buttons = ['AC', 'DEL', '=']
        matrices_row1 = ['MatA', 'MatB', 'MatC']
        matrices_row2 = ['MatD', 'MatE', 'MatF']

        buttons_grid = [row1_buttons, row2_buttons, row3_buttons, row4_buttons, row5_buttons, row6_buttons, row7_buttons]

        self.arrow_keys = {'↑': "up", '↓': "down", '←': "left", '→': "right"}
        special_buttons = {'DEL', 'AC'}
        self.row4_mappings = {'inv': "^(-1)"}

        row = 5
        col = 0
        for button_row in buttons_grid:
            for button in button_row:
                if button in self.arrow_keys:
                    b = tk.Button(self, text=button, **self.button_params_main, command=lambda t=button: self.on_click(t), height=2)
                elif button in special_buttons:
                    b = tk.Button(self, text=button, **self.button_params_other, command=lambda t=button: self.on_click(t), height=2)
                else:
                    b = tk.Button(self, text=button, **self.button_params, command=lambda t=button: self.on_click(t), height=2)

                b.grid(row=row, column=col, sticky="nsew")
                col += 1
                if col == 3:
                    col = 0
                    row += 1
            row += 1

        row = 3
        for row_matrix in [matrices_row1, matrices_row2]:
            col = 0
            for matrix in row_matrix:
                b = tk.Button(self, text=matrix, **self.button_params_main, command=lambda m=matrix: self.set_matrix(m), height=2)
                b.grid(row=row, column=col, sticky="nsew")
                col += 1
            row += 1

        for i in range(20):
            self.grid_rowconfigure(i, weight=1)
        for i in range(3):
            self.grid_columnconfigure(i)

        add_matrix_button = tk.Button(self, text="Add Matrix", command=self.add_matrix, **self.button_params_main, height=2)
        add_matrix_button.grid(row=19, column=0, columnspan=2, sticky="nsew")

        back_button = tk.Button(self, text="Back", command=lambda: self.controller.show_frame("StartPage"), **self.button_params_main, height=2)
        back_button.grid(row=19, column=2, columnspan=1, sticky="nsew")



    def on_click(self, text):
        print(f"Clicked: {text}")
        if text in self.arrow_keys:
            text = self.arrow_keys[text]
        if text in self.row4_mappings:
            text = self.row4_mappings[text]
        if text == "^(-1)":
            self.perform_inverse()
            return
        if text == "AC":
            self.display_var.set("")
            self.result_label.config(text="")
        elif text == "DEL":
            self.display_var.set(self.display_var.get()[:-1])
        elif text == "=":
            try:
                result = self.calculate()
                self.result_label.config(text=result)
            except Exception as e:
                self.result_label.config(text="Error")
                print(f"Calculation error: {e}")
        else:
            self.display_var.set(self.display_var.get() + text)

    def perform_inverse(self):
        operation = self.display_var.get()
        matrix_name = operation.strip()
        try:
            inverse_matrix = self.solver.inverse(matrix_name)
            self.result_label.config(text=f"{matrix_name}^-1 =\n{inverse_matrix}")
        except ValueError as e:
            self.result_label.config(text=str(e))

    def calculate(self):
        operation = self.display_var.get()
        result = eval(operation, {"__builtins__": None}, self.matrices)
        return result

    def add_matrix(self):
        self.matrix_input_page = MatrixInputPage(self, self.open_matrix_entry_page)

    def open_matrix_entry_page(self, rows, cols, matrix_name):
        self.matrix_entry_page = MatrixEntryPage(self, self.store_matrix)
        self.matrix_entry_page.set_matrix_details(rows, cols, matrix_name)

    def store_matrix(self, name, matrix):
        self.matrices[name] = np.array(matrix)
        self.solver.update_matrix(self.matrices['MatA'], self.matrices['MatB'], self.matrices['MatC'], self.matrices['MatD'], self.matrices['MatE'], self.matrices['MatF'])

    def set_matrix(self, name):
        current_text = self.operation_entry.get()
        new_text = f"{current_text}{name}"
        self.operation_entry.delete(0, tk.END)
        self.operation_entry.insert(0, new_text)
if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg="#293C4A")
    root.geometry("330x800")
    root.title("Standalone Calculator")

    # Initialize the Calculator frame
    calculator_frame = MatrixOperationPage(root, root)
    calculator_frame.pack(fill="both", expand=True)
    root.mainloop()