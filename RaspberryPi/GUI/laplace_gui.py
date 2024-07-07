import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
from tkinter import ttk
import math
from sympy import symbols, sympify, laplace_transform
from fourier_solver import get_laplace_transform, get_laplace_spectrum

class LaplaceTransform(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f0f0f0")
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
        
        ttk.Label(function_frame, text="f(t) = ").grid(row=0, column=0)
        self.function_entry = ttk.Entry(function_frame, textvariable=self.function_var, font=('Arial', 14))
        self.function_entry.grid(row=0, column=1, sticky="ew")

        # Transform button
        ttk.Button(self, text="Compute Laplace Transform", command=self.compute_transform).grid(row=1, column=0, pady=10)

        # Result display
        result_frame = ttk.Frame(self)
        result_frame.grid(row=2, column=0, pady=20, padx=20, sticky="ew")
        result_frame.columnconfigure(1, weight=1)
        
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
            ttk.Button(calc_frame, text=button, command=cmd).grid(row=row, column=col, sticky='nsew', padx=2, pady=2)
            col += 1
            if col > 5:
                col = 0
                row += 1

        # Help button
        ttk.Button(self, text="Help", command=self.show_help).grid(row=4, column=0, pady=10)

        # Back button
        ttk.Button(self, text="Back", command=lambda: self.controller.show_frame("StartPage")).grid(row=5, column=0, pady=10)

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
        expr = self.function_var.get()
        get_laplace_transform(expr, "t", "s")
        print(f"Expression: {expr}")
        self.controller.show_frame("ShowLaplaceTransform")


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
        ttk.Label(help_window, text=help_text, justify=tk.LEFT).pack(padx=20, pady=20)

# The rest of the code (ShowLaplaceTransform and LaplaceApp classes) remains the same

class ShowLaplaceTransform(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        img = tk.PhotoImage(file="integrals/laplace_transform.png")
        label = tk.Label(self, image=img, borderwidth=0)
        label.image = img
        label.pack()

        close_button = tk.Button(self, text="Close", command=lambda: self.controller.show_frame("LaplaceTransform"))
        close_button.pack()

        show_button = tk.Button(self, text="Show Spectrum", command=self.show_spectrum)
        show_button.pack()

    def show_spectrum(self):
        get_laplace_spectrum()
        print("Showing Laplace Spectrum")
        self.controller.show_frame("ShowLaplaceSpectrum")

class ShowLaplaceSpectrum(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        img = tk.PhotoImage(file="integrals/laplace_spectrum.png")
        label = tk.Label(self, image=img, borderwidth=0)
        label.image = img
        label.pack()

        close_button = tk.Button(self, text="Close", command=lambda: self.controller.show_frame("LaplaceTransform"))
        close_button.pack()