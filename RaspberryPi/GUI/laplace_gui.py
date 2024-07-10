import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
from tkinter import ttk
import math
from sympy import symbols, sympify, laplace_transform
from fourier_solver import get_laplace_transform

class LaplaceTransform(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#293C4A")  # Set background color
        self.controller = controller
        
        self.function_var = tk.StringVar(value="")
        self.result_var = tk.StringVar(value="")
        
        self.create_widgets()

    def create_widgets(self):
        self.columnconfigure(0, weight=1)

        # Function entry
        function_frame = ttk.Frame(self)
        function_frame.grid(row=0, column=0, pady=20, padx=20, sticky="ew")
        function_frame.columnconfigure(1, weight=1)
        
        ttk.Label(function_frame, text="f(t) = ", font=('sans-serif', 10, 'bold')).grid(row=0, column=0)
        self.function_entry = ttk.Entry(function_frame, textvariable=self.function_var, font=('sans-serif', 10, 'bold'), justify='right')
        self.function_entry.grid(row=0, column=1, sticky="ew")

        # Transform button
        ttk.Button(self, text="Compute Laplace Transform", command=self.compute_transform, style="TButton").grid(row=1, column=0, pady=40)

        # Result display
        #result_frame = ttk.Frame(self)
        #result_frame.grid(row=2, column=0, pady=20, padx=20, sticky="ew")
        #result_frame.columnconfigure(1, weight=1)
        
       

        # Calculator buttons
        calc_frame = ttk.Frame(self)
        calc_frame.grid(row=3, column=0, pady=20)
        
        buttons = [
            'AC', 'DEL', '(', ')', '^', 'sqrt',
            '7', '8', '9', '/', 'sin', 'cos',
            '4', '5', '6', '*', 'tan', 'exp',
            '1', '2', '3', '-', 'log', 'u(t)',
            '0', '.', 't', '+', 'e', 'δ(t)'
        ]
        
        row, col = 0, 0
        for button in buttons:
            cmd = lambda x=button: self.click(x)
            ttk.Button(calc_frame, text=button, command=cmd, style="Calc.TButton").grid(row=row, column=col, sticky='nsew', padx=2, pady=2)
            col += 1
            if col > 5:
                col = 0
                row += 1

        # Help button
        ttk.Button(self, text="Help", command=self.show_help, style="TButton").grid(row=4, column=0, pady=10)

        # Back button
        ttk.Button(self, text="Back", command=lambda: self.controller.show_frame("StartPage"), style="TButton").grid(row=5, column=0, pady=10)

    def click(self, key):
        if key == 'AC':
            self.function_var.set("")
        elif key == 'DEL':
            self.function_var.set(self.function_var.get()[:-1])
        elif key in ['sin', 'cos', 'tan', 'exp', 'log', 'sqrt']:
            self.function_var.set(self.function_var.get() + key + '(')
        elif key in ['u(t)', 'δ(t)']:
            self.function_var.set(self.function_var.get() + key)
        else:
            self.function_var.set(self.function_var.get() + key)

    def compute_transform(self):
        try:
            t, s = symbols('t s')
            expr = sympify(self.function_var.get())
            result = get_laplace_transform(expr, t, s)
            self.result_var.set(result)
        except Exception as e:
            self.result_var.set(f"Error: {str(e)}")

    def show_help(self):
        help_text = """
        Laplace Transform Calculator

        Enter a function of t to compute its Laplace transform.
        
        Examples:
        - t^2 : L{t^2} = 2/s^3
        - e^t : L{e^t} = 1/(s-1)
        - sin(t) : L{sin(t)} = 1/(s^2 + 1)
        
        Special functions:
        - u(t): Unit step function
        - δ(t): Dirac delta function

        Buttons:
        - AC: Clear all input
        - DEL: Delete last character

        Use the calculator buttons for easy input of functions and operations.
        """
        help_window = tk.Toplevel(self)
        help_window.title("Help")
        ttk.Label(help_window, text=help_text, justify=tk.LEFT, background="#293C4A", foreground="#BBB").pack(padx=20, pady=20)

# The rest of the code (ShowLaplaceTransform and LaplaceApp classes) remains the same

class ShowLaplaceTransform(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        ttk.Label(self, text="Laplace Transform Result", font=('sans-serif', 20, 'bold'), background="#293C4A", foreground="#BBB").pack(pady=10)
        ttk.Button(self, text="Back to Calculator", command=lambda: controller.show_frame("LaplaceTransform"), style="TButton").pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg="#293C4A", bd=10)
    root.geometry("330x800")
    root.title("Standalone Calculator")

    # Initialize the Calculator frame
    calculator_frame = LaplaceTransform(root, root)
    calculator_frame.pack(fill="both", expand=True)

    # Define styles
    style = ttk.Style()
    style.configure("TButton", font=('sans-serif', 10, 'bold'), background="#BBB", foreground="#000")
    style.configure("Calc.TButton", font=('sans-serif', 10, 'bold'), background="#BBB", foreground="#000", width=5)

    root.mainloop()
