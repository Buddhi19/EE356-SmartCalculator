import sys
import os  

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
from tkinter import ttk
from simultaneous_equations import Simul, SimultaneousEquations


class Simultaneous_solver_Frame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.equations = []
        self.answer = SimultaneousEquations()
        self.create_widgets()

    def create_widgets(self):
        self.configure(bg="#293C4A")

        self.equation_list = tk.Listbox(self, bg="#293C4A", fg="#FFF", font=('sans-serif', 15, 'bold'))
        self.equation_list.grid(row=0, column=0, columnspan=4, sticky="nsew")

        button_params_main = {'fg': '#000', 'bg': '#BBB', 'font': ('sans-serif', 13, 'bold')}

        add_button = tk.Button(self, text="Add Equation", command=lambda: Simultaneous_Frame(self, self.add_equation), **button_params_main, width=15)
        add_button.grid(row=1, column=0, sticky="nsew")

        remove_button = tk.Button(self, text="Remove Equation", command=self.remove_equation, **button_params_main, width=14)
        remove_button.grid(row=1, column=1, sticky="nsew")

        solve_equations_button = tk.Button(self, text="Solve Equations", command=self.solve_equations, **button_params_main, width=15)
        solve_equations_button.grid(row=2, column=0, sticky="nsew")

        back_button = tk.Button(self, text="Back", command=lambda: self.controller.show_frame("StartPage"), **button_params_main, width=14)
        back_button.grid(row=2, column=1, sticky="nsew")

        start_again_button = tk.Button(self, text="Start Again", command=self.clear_all_equations, **button_params_main, width=30)
        start_again_button.grid(row=3, column=0, columnspan=2, sticky="nsew")

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=0)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)

    def add_equation(self, equation):
        self.equations.append(equation)
        print(self.equations)
        self.update_equation_list()

    def remove_equation(self):
        selected_indices = self.equation_list.curselection()
        if selected_indices:
            for index in selected_indices[::-1]:
                del self.equations[index]
            self.update_equation_list()

    def solve_equations(self):
        ans = self.answer.simultaneous_solver(self.equations)
        print(ans)
        for key in ans:
            self.equation_list.insert(tk.END, f"{key} = {ans[key]}")

    def clear_all_equations(self):
        self.equations.clear()
        self.update_equation_list()

    def update_equation_list(self):
        self.equation_list.delete(0, tk.END)
        for eq in self.equations:
            self.equation_list.insert(tk.END, eq)

    def show_equations(self):
        self.update_equation_list()


class Simultaneous_Frame(tk.Toplevel):
    def __init__(self, parent, callback):
        super().__init__(parent)
        self.callback = callback
        self.solver = Simul()
        self.display_var = tk.StringVar()
        self.create_widgets()

    def create_widgets(self):
        self.button_params = {'fg': '#BBB', 'bg': '#3C3636', 'font': ('sans-serif', 15, 'bold')}
        self.button_params_main = {'bd': 5, 'fg': '#000', 'bg': '#BBB', 'font': ('sans-serif', 15, 'bold')}
        self.button_params_other = {'fg': '#000', 'bg': '#db701f', 'font': ('sans-serif', 15, 'bold')}

        entry = ttk.Entry(self, textvariable=self.display_var, font=('sans-serif', 20, 'bold'), justify='right', state='readonly', style="Custom.TEntry")
        entry.grid(row=0, column=0, columnspan=8, padx=0, pady=15, sticky="nsew")
        
        self.configure(bg="#293C4A")

        row1_buttons = ['←', '→', 'A', 'B', 'C', 'D']
        row2_buttons = ['U', 'V', 'W', 'X', 'Y', 'Z']
        row3_buttons = ['sin', 'cos', 'tan', 'ln', '(', ')']
        row4_buttons = ['7', '8', '9', '/', '*', 'hyp']
        row5_buttons = ['4', '5', '6', '^',  '+', '\u00B2\u221A']
        row6_buttons = ['1', '2', '3', 'π', '-', '=']
        row7_buttons = ['0', '.', 'EXP', 'DEL', 'AC']

        buttons_grid = [row1_buttons, row2_buttons, row3_buttons, row4_buttons, row5_buttons, row6_buttons, row7_buttons]

        self.arrow_keys = {'←': "left", '→': "right"}
        special_buttons = {'DEL', 'AC'}

        row = 1
        for row_buttons in buttons_grid:
            col = 0
            for button in row_buttons:
                if button in self.arrow_keys:
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

        back_button = tk.Button(self, text="Back", command=lambda: self.destroy(), **self.button_params_main)
        back_button.grid(row=8, column=0, columnspan=3, sticky="nsew")

        add_button = tk.Button(self, text="Add", **self.button_params_main)
        add_button.grid(row=8, column=3, columnspan=3, sticky="nsew")
        add_button.bind("<Button-1>", self.on_click)

    def on_click(self, event):
        button_text = event.widget.cget("text")
        if button_text in self.arrow_keys:
            button_text = self.arrow_keys[button_text]
        if button_text == "Add":
            data = self.solver.user_input(button_text)
            if data:
                self.callback(data)
                self.destroy()
            else:
                self.display_var.set(self.solver.showing_exp)
        self.solver.user_input(button_text)
        self.display_var.set(self.solver.showing_exp)


if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg="#293C4A", bd=10)
    root.geometry("330x800")
    root.title("Standalone Calculator")

    calculator_frame = Simultaneous_solver_Frame(root, root)
    calculator_frame.pack(fill="both", expand=True)
    root.mainloop()
