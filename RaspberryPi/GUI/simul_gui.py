import tkinter as tk
from tkinter import ttk

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

        show_button = ttk.Button(self, text="Show Equations", command=self.show_equations)
        show_button.pack(side=tk.RIGHT, fill=tk.X, expand=True)

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
        self.display_var = tk.StringVar()
        self.create_widgets()
    
    def create_widgets(self):
        entry = ttk.Entry(self, textvariable=self.display_var, font=('Arial', 20), justify='right', state='readonly')
        entry.grid(row=0, column=0, columnspan=8, sticky="nsew")

        buttons = [
            'left', 'right', '', 'MODE', 'DEL', 'AC', '', '',
            'x1', 'x2', 'x3', 'x4', 'log', '', '', '',
            '7', '8', '9', '/', 'sin', 'cos', 'tan', 'hyp',
            '4', '5', '6', '*', 'ln', '(', ')', '√',
            '1', '2', '3', '-', '^', 'x⁻¹', 'pi', 'nCr',
            '0', '.', '±', '+', 'plot', 'EXP', 'x10^x', '='
        ]

        row = 1
        col = 0
        for button in buttons:
            if button != '':
                b = ttk.Button(self, text=button, width=5)
                b.grid(row=row, column=col, sticky="nsew")
                b.bind("<Button-1>", self.on_click)
            col += 1
            if col == 8:
                col = 0
                row += 1

        for i in range(6):
            self.grid_rowconfigure(i, weight=1)
        for i in range(8):
            self.grid_columnconfigure(i, weight=1)

        back_button = ttk.Button(self, text="Back", command=lambda: self.controller.show_frame("Simultaneous_solver_Frame"))
        back_button.grid(row=7, column=0, columnspan=4, sticky="nsew")

        add_button = ttk.Button(self, text="Add", command=self.add_equation)
        add_button.grid(row=7, column=4, columnspan=4, sticky="nsew")

    def on_click(self, event):
        button_text = event.widget.cget("text")
        current_text = self.display_var.get()

        if button_text == 'AC':
            self.display_var.set("")
        elif button_text == 'DEL':
            self.display_var.set(current_text[:-1])
        else:
            self.display_var.set(current_text + button_text)

    def calculate(self):
        # This is a placeholder for the calculation logic.
        pass

    def add_equation(self):
        equation = self.display_var.get()
        if equation:
            self.controller.frames["Simultaneous_solver_Frame"].add_equation(equation)
            self.display_var.set("")