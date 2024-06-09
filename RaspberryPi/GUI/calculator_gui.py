import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main_controller import Calculator
import tkinter as tk
from tkinter import ttk
import math

class Calculator_Frame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#293C4A")
        self.controller = controller
        self.display_var = tk.StringVar()
        self.create_widgets()
        self.Cal = Calculator()

        # Style for ttk.Entry
        entry = ttk.Entry(self, textvariable=self.display_var, font=('sans-serif', 20, 'bold'), justify='right', state='readonly')
        entry.grid(row=0, column=0, columnspan=8, padx=10, pady=20, sticky="nsew")


    def create_widgets(self):
        self.button_params = { 'fg': '#BBB', 'bg': '#3C3636', 'font': ('sans-serif', 15, 'bold')}
        self.button_params_main = {'bd': 5, 'fg': '#000', 'bg': '#BBB', 'font': ('sans-serif', 15, 'bold')}
        self.button_params_other = { 'fg': '#000', 'bg':'#db701f', 'font': ('sans-serif', 15, 'bold')}

        row1_buttons = ['shift', 'MODE', '', '↑','', 'ln','%']
        row1_shift_buttons = ['sin⁻¹', 'cos⁻¹', 'tan⁻¹']
        row2_buttons = ['+', '-', '←', '', '→', 'x!', 'π']
        row3_buttons = ['x', '/', '', '↓', '', 'd/dx', '∫']
        row4_buttons = ['7', '8', '9', 'x^n', 'sin', 'cos', 'tan']
        row5_buttons = ['4', '5', '6', '\u00B2\u221A', 'log', '(', ')']
        row6_buttons = ['1', '2', '3', 'e^x', 'hyp', 'DEL', 'AC']
        row7_buttons = ['0', '.', 'EXP', 'x\u207b\xb9', 'nCr','long', '=']

        buttons_grid = [row1_buttons, row2_buttons, row3_buttons, row4_buttons, row5_buttons, row6_buttons, row7_buttons]

        arrow_keys = {'↑', '↓', '←', '→'}
        special_buttons = {'DEL', 'AC', '='}

        row = 1
        for row_buttons in buttons_grid:
            col = 0
            for button in row_buttons:
                if button in arrow_keys:
                    b = tk.Button(self, text=button, **self.button_params_main, width=5)
                elif button in special_buttons:
                    b = tk.Button(self, text=button, **self.button_params_other, width=5)
                elif button != '':
                    b = tk.Button(self, text=button, **self.button_params, width=5)
                else:
                    col += 1
                    continue

                b.grid(row=row, column=col, sticky="nsew")
                b.bind("<Button-1>", self.on_click)
                col += 1
                if col == 8:
                    col = 0
                    row += 1
            row += 1
            
        for i in range(8):
            self.grid_rowconfigure(i, weight=1)
        for i in range(9):
            self.grid_columnconfigure(i, weight=1)

    def on_click(self, event):
        text = event.widget.cget("text")
        self.Cal.user_input(text)
        self.display_var.set(self.Cal.showing_exp)

if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg="#293C4A", bd=10)
    root.geometry("480x800")
    root.title("Standalone Calculator")

    # Initialize the Calculator frame
    calculator_frame = Calculator_Frame(root, root)
    calculator_frame.pack(fill="both", expand=True)

    root.mainloop()
