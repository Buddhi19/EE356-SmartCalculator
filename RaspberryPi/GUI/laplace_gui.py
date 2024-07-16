import os
import sys

parent_dir = os.path.dirname(os.path.abspath(__file__))

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
from tkinter import ttk
import math
from sympy import symbols, sympify, laplace_transform
from fourier_solver import get_laplace_transform, get_laplace_spectrum

class LaplaceTransform(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#293C4A")  # Set background color
        self.controller = controller
        
        self.function_var = tk.StringVar(value="")
        self.result_var = tk.StringVar(value="")
        
        self.create_widgets()

    def create_widgets(self):
        self.configure(bg="#293C4A")
        self.button_params = { 'fg': '#BBB', 'bg': '#3C3636', 'font': ('sans-serif', 11, 'bold')}
        self.button_params_main = { 'fg': '#000', 'bg': '#BBB', 'font': ('sans-serif', 11, 'bold')}
        self.button_params_other = { 'fg': '#000', 'bg':'#db701f', 'font': ('Arial', 11, 'bold')}
        self.columnconfigure(0, weight=1)

        # Function entry
        function_frame = ttk.Frame(self)
        function_frame.grid(row=0, column=0, pady=20, sticky="ew")
        function_frame.columnconfigure(1, weight=1)
        
        ttk.Label(function_frame, text="f(t) = ", font=('sans-serif', 15, 'bold')).grid(row=0, column=0)
        self.function_entry = ttk.Entry(function_frame, textvariable=self.function_var, font=('sans-serif', 15, 'bold'), justify='right', width=20)
        self.function_entry.grid(row=0, column=1, sticky="ew")

        # Transform button
        tk.Button(self, text="Compute Laplace Transform", command=self.compute_transform, **self.button_params_main, width=30).grid(row=1, column=0, pady=20)

        # Calculator buttons
        calc_frame = ttk.Frame(self)
        calc_frame.grid(row=2, column=0, pady=20)
        
        buttons = [
            '←', '→', '(', ')', 
            't', 'δ(t)', 'u(t)', '^',
            'sqrt', 'sin', 'cos', 'tan',
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',  
            '0', '.', 'e', '+', 
            'AC', 'DEL', 'log', 'exp'
        ]

        special_buttons = {'DEL', 'AC', '='}
        self.arrow_keys = {'↑': "up", '↓': "down", '←': "left", '→': "right"}
        
        row, col = 0, 0
        for button in buttons:
            if button in self.arrow_keys:
                cmd = lambda x=button: self.click(x)
                tk.Button(calc_frame, text=button, command=cmd, **self.button_params_main, width=9, height=3).grid(row=row, column=col, sticky='nsew')
            elif button in special_buttons:
                cmd = lambda x=button: self.click(x)
                tk.Button(calc_frame, text=button, command=cmd, **self.button_params_other, width=9, height=3).grid(row=row, column=col, sticky='nsew')
            else:
                cmd = lambda x=button: self.click(x)
                tk.Button(calc_frame, text=button, command=cmd, **self.button_params, width=9, height=3).grid(row=row, column=col, sticky='nsew')
            col += 1
            if col > 3:
                col = 0
                row += 1

        # Other buttons
        other_buttons = ['Help', 'Back']
        other_buttons_frame = ttk.Frame(self)
        other_buttons_frame.grid(row=3, column=0, pady=10, sticky="ew")
        
        other_buttons_frame.columnconfigure(0, weight=1)
        other_buttons_frame.columnconfigure(1, weight=1)
        
        for i, button in enumerate(other_buttons):
            if button == 'Help':
                cmd = lambda x=button: self.show_help()
            else:
                cmd = lambda x=button: self.controller.show_frame("StartPage")
            tk.Button(other_buttons_frame, text=button, command=cmd, **self.button_params_main,width=20).grid(row=0, column=i, sticky="ew")

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
        t = "t"
        s = "s"
        print(f"Expression: {expr}")
        result = get_laplace_transform(expr, t, s)
        if result == "Error":
            self.result_var.set("Invalid input")
        self.controller.show_frame("ShowLaplaceTransform")

    def show_help(self):
        help_text = """
        Laplace Transform Calculator

        Enter a function of t to compute its Laplace 
        transform.
        
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

        Use the calculator buttons for easy input of 
        functions and operations.
        """
        help_window = tk.Toplevel(self)
        help_window.title("Help")
        help_window.configure(bg="#293C4A")
        help_window.geometry("330x500")
        
        help_label = tk.Label(help_window, text=help_text, justify=tk.LEFT, bg="#293C4A", fg="#BBB", font=('sans-serif', 10, 'bold'))
        help_label.pack(padx=10, pady=0)

class ShowLaplaceTransform(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        img = tk.PhotoImage(file=os.path.join(parent_dir, "integrals", "laplace_transform.png"))
        label = tk.Label(self, image=img, borderwidth=0)
        label.image = img
        label.pack()

        close_button = tk.Button(self, text="Close", command=lambda: self.controller.show_frame("LaplaceTransform"))
        close_button.pack()

        show_button = tk.Button(self, text="Show Spectrum", command=self.show_spectrum)
        show_button.pack()

    def show_spectrum(self):
        ans = get_laplace_spectrum()
        if ans == "Error":
            print("Error in generating Laplace Spectrum")
            return
        print("Showing Laplace Spectrum")
        self.controller.show_frame("ShowLaplaceSpectrum")

class ShowLaplaceSpectrum(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        img = tk.PhotoImage(file=os.path.join(parent_dir, "integrals", "laplace_spectrum.png"))
        label = tk.Label(self, image=img, borderwidth=0)
        label.image = img
        label.pack()

        close_button = tk.Button(self, text="Close", command=lambda: self.controller.show_frame("LaplaceTransform"))
        close_button.pack()

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
