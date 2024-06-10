import sys
import os  

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
from tkinter import ttk
from simultaneous_equations import Simul


class Simultaneous_solver_Frame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.equations = []
        self.create_widgets()

    def create_widgets(self):
        self.equation_list = tk.Listbox(self)
        self.equation_list.pack(fill=tk.BOTH, expand=True)

        add_button = ttk.Button(self, text="Add Equation", command=lambda: self.controller.show_frame("Simultaneous_Frame"))
        add_button.pack(side=tk.LEFT, fill=tk.X, expand=True)

        solve_equations_button = ttk.Button(self, text="Solve Equations")
        solve_equations_button.pack(side=tk.RIGHT, fill=tk.X, expand=True)

        back_button = ttk.Button(self, text="Back", command=lambda: self.controller.show_frame("StartPage"))
        back_button.pack(side=tk.RIGHT, fill=tk.X, expand=True) 

    def add_equation(self, equation):
        self.equations.append(equation)
        self.update_equation_list()

    def update_equation_list(self):
        self.equation_list.delete(0, tk.END)
        for eq in self.equations:
            self.equation_list.insert(tk.END, eq)

    def show_equations(self):
        self.update_equation_list()

class Simultaneous_Frame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.solver = Simul()
        self.display_var = tk.StringVar()
        self.create_widgets()
    
    # Style for ttk.Entry
        entry = ttk.Entry(self, textvariable=self.display_var, font=('sans-serif', 20, 'bold'), justify='right', state='readonly', style="Custom.TEntry")
        entry.grid(row=0, column=0, columnspan=8, padx=0, pady=15, sticky="nsew")
        
        # Set the background color of the frame to match the entry box     
        self.configure(bg="#293C4A")

    def create_widgets(self):
        
        self.button_params = { 'fg': '#BBB', 'bg': '#3C3636', 'font': ('sans-serif', 15, 'bold')}
        self.button_params_main = {'bd': 5, 'fg': '#000', 'bg': '#BBB', 'font': ('sans-serif', 15, 'bold')}
        self.button_params_other = { 'fg': '#000', 'bg':'#db701f', 'font': ('sans-serif', 15, 'bold')}

        
        row1_buttons =['mode', '', '←', '→', '', '']
        row2_buttons =['x', 'y', 'z', 'log', '+', '-']
        row3_buttons =['sin', 'cos', 'tan', 'ln', '/', '*']
        row4_buttons =['7', '8', '9', '(', ')', 'hyp']
        row5_buttons =['4', '5', '6', '^',  'x⁻¹', '\u00B2\u221A']
        row6_buttons =['1', '2', '3', 'x10^x', 'π', '=']
        row7_buttons =['0', '.', 'EXP', 'plot','DEL' , 'AC']

        buttons_grid = [row1_buttons, row2_buttons, row3_buttons, row4_buttons, row5_buttons, row6_buttons,row7_buttons]

        arrow_keys = { '←', '→'}
        special_buttons = {'DEL', 'AC'}

        row = 1
        for row_buttons in buttons_grid:
            col = 0
            for button in row_buttons:
                if button in arrow_keys:
                    b = tk.Button(self, text=button, **self.button_params_main, width=5)
                elif button in special_buttons:
                    b = tk.Button(self, text=button, **self.button_params_other, width=5)
                else:
                    b = tk.Button(self, text=button, **self.button_params, width=5)
                

                b.grid(row=row, column=col, sticky="nsew")
                b.bind("<Button-1>", self.on_click)
                col += 1
                if col == 8:
                    col = 0
                    row += 1
            row += 1


        for i in range(8):
            self.grid_rowconfigure(i, weight=1)
        for i in range(6):
            self.grid_columnconfigure(i, weight=1)

        back_button = ttk.Button(self, text="Back", command=lambda: self.controller.show_frame("Simultaneous_solver_Frame"))
        back_button.grid(row=8, column=0, columnspan=3, sticky="nsew")

        add_button = ttk.Button(self, text="Add", command=self.add_equation)
        add_button.grid(row=8, column=3, columnspan=3, sticky="nsew")

    def on_click(self, event):
        button_text = event.widget.cget("text")
        if button_text == "add":
            data = self.solver.user_input(button_text)
            
        self.solver.user_input(button_text)
        self.display_var.set(self.solver.showing_exp)

        

    def calculate(self):
        # This is a placeholder for the calculation logic.
        pass

    def add_equation(self):
        equation = self.display_var.get()
        if equation:
            self.controller.frames["Simultaneous_solver_Frame"].add_equation(equation)
            self.display_var.set("")