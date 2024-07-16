import os
import sys

parent_dir = os.path.dirname(os.path.abspath(__file__))

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from z_transform_solver import get_z_transform

class DiscreteSignalCalculator(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#293C4A")
        self.controller = controller
        self.current_input = tk.StringVar()
        self.signal = []

        self.create_widgets()

    def create_widgets(self):
        self.configure(bg="#293C4A")
        self.button_params = {'fg': '#BBB', 'bg': '#3C3636', 'font': ('sans-serif', 11, 'bold')}
        self.button_params_main = {'fg': '#000', 'bg': '#BBB', 'font': ('sans-serif', 11, 'bold')}
        self.button_params_other = {'fg': '#000', 'bg': '#db701f', 'font': ('Arial', 11, 'bold')}
        self.columnconfigure(0, weight=1)

        # Display area
        display_frame = ttk.Frame(self)
        display_frame.grid(row=0, column=0, pady=20, sticky="ew", ipady=10)
        display_frame.columnconfigure(1, weight=1)

        self.display = tk.Entry(display_frame, font=('sans-serif', 20, 'bold'), justify='right', textvariable=self.current_input)
        self.display.grid(row=0, column=0, columnspan=4, sticky="ew")

        # Buttons
        calc_frame = ttk.Frame(self)
        calc_frame.grid(row=1, column=0, pady=20)

        buttons = [
            '←', '→', '(', ')',
            'sin','cos','tan','sqrt',
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', 'n', '+',
            'AC', 'DEL', '^', '='
        ]

        special_buttons = {'DEL', 'AC', '='}
        self.arrow_keys = {'↑': "up", '↓': "down", '←': "left", '→': "right"}

        row, col = 0, 0
        for button in buttons:
            if button in self.arrow_keys:
                cmd = lambda x=button: self.click(x)
                tk.Button(calc_frame, text=button, command=cmd, **self.button_params_main, width=9, height=3).grid(row=row, column=col, sticky="nsew")
            elif button in special_buttons:
                cmd = lambda x=button: self.click(x)
                tk.Button(calc_frame, text=button, command=cmd, **self.button_params_other, width=9, height=3).grid(row=row, column=col, sticky="nsew")
            else:
                cmd = lambda x=button: self.click(x)
                tk.Button(calc_frame, text=button, command=cmd, **self.button_params, width=9, height=3).grid(row=row, column=col, sticky="nsew")
            col += 1
            if col > 3:
                col = 0
                row += 1

        # Compute Z Transform button
        tk.Button(self, text="Compute Z Transform", command=self.calculate_z_transform, **self.button_params_main, width=20, height=2).grid(row=3, column=0, pady=10)

        # Back button
        tk.Button(self, text="Back", command=lambda: self.controller.show_frame("StartPage"), **self.button_params_main, width=15, height=2).grid(row=4, column=0, pady=10)

    def click(self, key):
        if key == 'AC':
            self.current_input.set("")
        elif key == 'DEL':
            self.current_input.set(self.current_input.get()[:-1])
        elif key == 'n':
            if self.current_input.get() and self.current_input.get()[-1].isdigit():
                self.current_input.set(self.current_input.get() + '*n')
            else:
                self.current_input.set(self.current_input.get() + 'n')
        elif key in ['sin', 'cos', 'tan', 'sqrt']:
            self.current_input.set(self.current_input.get() + key + '(')
        elif key == '^':
            if self.current_input.get() and self.current_input.get()[-1] in ('n', ')', ']', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
                self.current_input.set(self.current_input.get() + '^')
            else:
                messagebox.showerror("Error", "^ must follow n or a number")
        else:
            self.current_input.set(self.current_input.get() + str(key))

    def calculate_z_transform(self):
        try:
            result = get_z_transform(self.signal)
            messagebox.showinfo("Z-Transform Result", result)
        except Exception as e:
            messagebox.showerror("Error", f"Error calculating Z-transform: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg="#293C4A", bd=10)
    root.geometry("330x800")
    root.title("Discrete Signal Calculator")

    calculator_frame = DiscreteSignalCalculator(root, root)
    calculator_frame.pack(fill="both", expand=True)

    style = ttk.Style()
    style.configure("TButton", font=('sans-serif', 10, 'bold'), background="#BBB", foreground="#000")
    style.configure("Calc.TButton", font=('sans-serif', 10, 'bold'), background="#BBB", foreground="#000", width=5)

    root.mainloop()
