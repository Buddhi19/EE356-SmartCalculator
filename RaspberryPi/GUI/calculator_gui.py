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
        entry.grid(row=0, column=0, columnspan=7, padx=0, pady=15, sticky="nsew")


    def create_widgets(self):
        self.button_params = { 'fg': '#BBB', 'bg': '#3C3636', 'font': ('sans-serif', 15, 'bold')}
        self.button_params_main = {'bd': 5, 'fg': '#000', 'bg': '#BBB', 'font': ('sans-serif', 15, 'bold')}
        self.button_params_other = { 'fg': '#000', 'bg':'#db701f', 'font': ('sans-serif', 15, 'bold')}

        row1_buttons = ['shift', 'MODE', '', '↑','', 'ln','%']
        row1_shift_buttons = ['sin⁻¹', 'cos⁻¹', 'tan⁻¹']
        row2_buttons = ['+', '-', '←', '', '→', 'x!', 'π']
        row3_buttons = ['*', '/', '', '↓', '', 'd/dx', '∫']
        row4_buttons = ['7', '8', '9', 'x^n', 'sin', 'cos', 'tan']
        row5_buttons = ['4', '5', '6','\u00B2\u221A' , 'log', '(', ')']
        row6_buttons = ['1', '2', '3', 'e^x', 'hyp', 'DEL', 'AC']
        row7_buttons = ['0', '.', 'EXP', 'x\u207b\xb9', 'nCr','\u2044', '=']

        buttons_grid = [row1_buttons, row2_buttons, row3_buttons, row4_buttons, row5_buttons, row6_buttons, row7_buttons]

        self.arrow_keys = {'↑':"up", '↓':"down", '←':"left", '→':"right"}
        special_buttons = {'DEL', 'AC', '='}

        row = 1
        for row_buttons in buttons_grid:
            col = 0
            for button in row_buttons:
                if button in self.arrow_keys:
                    b = tk.Button(self, text=button, **self.button_params_main, width=4)
                elif button in special_buttons:
                    b = tk.Button(self, text=button, **self.button_params_other)
                else:
                    b = tk.Button(self, text=button, **self.button_params)
                

                b.grid(row=row, column=col, sticky="nsew")
                b.bind("<Button-1>", self.on_click)
                col += 1
                if col == 8:
                    col = 0
                    row += 1
            row += 1
            
        for i in range(8):
            self.grid_rowconfigure(i)
        for i in range(9):
            self.grid_columnconfigure(i)

        back_button = tk.Button(self, text="Back", command=lambda: self.controller.show_frame("StartPage"), **self.button_params_main)
        back_button.grid(row=8, column=0, columnspan=7, sticky="nsew")

    def on_click(self, event):
        text = event.widget.cget("text")
        if text in self.arrow_keys:
            text = self.arrow_keys[text]
        if text == "MODE":
            ModeSelectionPopup(self, self.set_mode)
        else:
            self.Cal.user_input(text)
            self.display_var.set(self.Cal.showing_exp)

    def set_mode(self, mode):
        print(f"Selected Mode: {mode}")
        self.MODE = mode

class ModeSelectionPopup(tk.Toplevel):
    def __init__(self, parent, callback):
        super().__init__(parent)
        self.callback = callback

        self.overrideredirect(True)
        self.mode_list = [
            "Calculate", "Complex", "Equation", "Matrix"
            # Add more modes as needed
        ]

        self.create_mode_buttons()
        
    def create_mode_buttons(self):
        for mode in self.mode_list:
            button = ttk.Button(self, text=mode, command=lambda m=mode: self.select_mode(m))
            button.pack(fill=tk.X, padx=5, pady=5)

    def select_mode(self, mode):
        self.callback(mode)
        self.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg="#293C4A", bd=10)
    root.geometry("480x800")
    root.title("Standalone Calculator")

    # Initialize the Calculator frame
    calculator_frame = Calculator_Frame(root, root)
    calculator_frame.pack(fill="both", expand=True)

    root.mainloop()
