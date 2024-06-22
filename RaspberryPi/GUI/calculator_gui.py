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
        self.answer = tk.StringVar()
        self.create_widgets()
        self.Cal = Calculator()


        # Style for ttk.Entry
        entry = ttk.Entry(self, textvariable=self.display_var, font=('Arial', 20, 'bold'), justify='right', state='readonly')
        entry.grid(row=0,rowspan=11, column=0, columnspan=9, sticky="nsew")

    def create_widgets(self):
        self.button_params = { 'fg': '#BBB', 'bg': '#3C3636', 'font': ('Arial', 11, 'bold')}
        self.button_params_main = {'bd': 5, 'fg': '#000', 'bg': '#BBB', 'font': ('Arial', 11, 'bold')}
        self.button_params_other = { 'fg': '#000', 'bg':'#db701f', 'font': ('Arial', 11, 'bold')}

        self.row1_buttons = ['', '', '', '↑','', 'ln']
        self.row1_shift_buttons = ['shifted', 'MODE', '', '↑','', 'ln']
        self.row2_buttons = ['', 'pi', '←', '↓', '→', 'log']
        self.row3_buttons = ['(', ')', '^','x!' , '√', 'nCr']
        self.row4_buttons = ['7', '8', '9', 'tan', 'sin', 'cos']
        self.row3b = ['', '', 'j', 'tan\u207b\xb9', 'sin\u207b\xb9', 'cos\u207b\xb9']
        self.row5_buttons = ['4', '5', '6', '+', '-',"AC"]
        self.row6_buttons = ['1', '2', '3', "*","/", 'DEL']
        self.row7_buttons = ['0', '.', 'e', 'x\u207b\xb9', '=']

        self.row4_mappings = {
            'tan\u207b\xb9': 'atan','sin\u207b\xb9': 'asin', 'cos\u207b\xb9': 'acos','x!':'!','x\u207b\xb9':'^(-1)'
        }

        self.buttons_grid = [
            self.row1_buttons, self.row2_buttons, self.row3_buttons,self.row3b, self.row4_buttons,
            self.row5_buttons, self.row6_buttons, self.row7_buttons
        ]
        self.arrow_keys = {'↑':"up", '↓':"down", '←':"left", '→':"right"}
        special_buttons = {'DEL', 'AC', '='}

        row = 11
        for row_buttons in self.buttons_grid:
            col = 0
            for button in row_buttons:
                if button in self.arrow_keys:
                    b = tk.Button(self, text=button, **self.button_params_main, width=6, height=3)
                elif button in special_buttons:
                    b = tk.Button(self, text=button, **self.button_params_other, width=6, height=3)
                else:
                    b = tk.Button(self, text=button, **self.button_params, width=6, height=3)
                

                b.grid(row=row, column=col, sticky="nsew")
                b.bind("<Button-1>", self.on_click)
                col += 1
                if col == 8:
                    col = 0
                    row += 1
            row += 1
            
        for i in range(20):
            self.grid_rowconfigure(i,weight=1)
        for i in range(6):
            self.grid_columnconfigure(i)

        back_button = tk.Button(self, text="Back", command=lambda: self.controller.show_frame("StartPage"), **self.button_params_main)
        back_button.grid(row=19, column=0, columnspan=2, sticky="nsew")

    def on_click(self, event):
        text = event.widget.cget("text")
        print(f"Clicked: {text}")
        if text in self.arrow_keys:
            text = self.arrow_keys[text]
        if text in self.row4_mappings:
            text = self.row4_mappings[text]
        if text == "^(-1)":
            self.Cal.result += text
            self.Cal.convert_to_understandable()
            self.display_var.set(self.Cal.showing_exp)
            return
        self.Cal.user_input(text)
        if text == "=" or text == "AC":
            self.answer.set(self.Cal.result)
            self.Cal.update_pointer()
        self.display_var.set(self.Cal.showing_exp)

    def update_keys(self):
        if self.shift:
            self.shift = False
            
    def set_mode(self, mode):
        print(f"Selected Mode: {mode}")
        self.MODE = mode


if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg="#293C4A", bd=10)
    root.geometry("330x800")
    root.title("Standalone Calculator")

    # Initialize the Calculator frame
    calculator_frame = Calculator_Frame(root, root)
    calculator_frame.pack(fill="both", expand=True)

    root.mainloop()
    