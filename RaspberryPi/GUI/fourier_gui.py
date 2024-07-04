import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
from tkinter import ttk
import math
from fourier_solver import FourierSolver, get_fourier_transform

class FourierTransform(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#293C4A")
        self.controller = controller
        self.display_var = tk.StringVar(value="Function to transform")
        self.display_initial_variable = tk.StringVar(value="Initial variable")
        self.display_final_variable = tk.StringVar(value="Final variable")
        self.create_widgets()

        self.fourier_solver = FourierSolver()

        # Entry widgets
        self.entry1 = ttk.Entry(self, textvariable=self.display_var, font=('Arial', 20, 'bold'), justify='right', state='readonly')
        self.entry1.grid(row=0, rowspan=5, column=0, columnspan=9, sticky="nsew")

        self.entry2 = ttk.Entry(self, textvariable=self.display_initial_variable, font=('Arial', 10, 'bold'), justify='right', state='readonly')
        self.entry2.grid(row=5, rowspan=3, column=0, columnspan=9, sticky="nsew")

        self.entry3 = ttk.Entry(self, textvariable=self.display_final_variable, font=('Arial', 10, 'bold'), justify='right', state='readonly')
        self.entry3.grid(row=8, rowspan=3, column=0, columnspan=9, sticky="nsew")

        self.current_entry = None  # To track currently focused entry

        # Key bindings
        self.bind_keys()

    def create_widgets(self):
        # Button configurations and grid layout (example buttons)
        self.button_params = {'fg': '#BBB', 'bg': '#3C3636', 'font': ('Arial', 11, 'bold')}
        self.button_params_main = {'bd': 5, 'fg': '#000', 'bg': '#BBB', 'font': ('Arial', 11, 'bold')}
        self.button_params_other = {'fg': '#000', 'bg': '#db701f', 'font': ('Arial', 11, 'bold')}

        self.row1_buttons = ['', '', '', '↑', '', 'ln']
        self.row2_buttons = ['', 'pi', '←', '↓', '→', 'log']
        self.row3_buttons = ['(', ')', 'w', 'x', 'y', 't']
        self.row4_buttons = ['7', '8', '9', '', '', '^']
        self.row3b = ['tan', 'sin', 'cos', 'tan\u207b\xb9', 'sin\u207b\xb9', 'cos\u207b\xb9']
        self.row5_buttons = ['4', '5', '6', '+', '-', "AC"]
        self.row6_buttons = ['1', '2', '3', "*", "/", 'DEL']
        self.row7_buttons = ['0', '.', 'e', 'x\u207b\xb9', 'Transform']

        self.row4_mappings = {
            'tan\u207b\xb9': 'atan', 'sin\u207b\xb9': 'asin', 'cos\u207b\xb9': 'acos', 'x!': '!', 'x\u207b\xb9': '^(-1)'
        }

        self.variables = ['w', 'x', 'y', 't']

        self.buttons_grid = [
            self.row1_buttons, self.row2_buttons, self.row3_buttons, self.row3b, self.row4_buttons,
            self.row5_buttons, self.row6_buttons, self.row7_buttons
        ]
        self.arrow_keys = {'↑': "up", '↓': "down", '←': "left", '→': "right"}
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
            self.grid_rowconfigure(i, weight=1)
        for i in range(6):
            self.grid_columnconfigure(i)

        back_button = tk.Button(self, text="Back", command=lambda: self.controller.show_frame("StartPage"), **self.button_params_main)
        back_button.grid(row=19, column=0, columnspan=2, sticky="nsew")

    def on_click(self, event):
        text = event.widget.cget("text")

        if text == "Transform":
            if self.display_initial_variable.get() == "Initial variable" or self.display_final_variable.get() == "Final variable":
                return
            if self.display_var.get() == "Function to transform":
                return
            exp = self.fourier_solver.final_expression()
            t = self.display_initial_variable.get()
            w = self.display_final_variable.get()
            get_fourier_transform(exp, t, w)
            self.controller.show_frame("ShowFourierSpectrum")
            return

        if self.current_entry == self.entry2:
            if text in ["AC", "DEL"]:
                self.display_initial_variable.set("Initial variable")
                return
            if text in self.variables:
                self.display_initial_variable.set(text)
        elif self.current_entry == self.entry3:
            if text in ["AC", "DEL"]:
                self.display_final_variable.set("Final variable")
                return
            if text in self.variables:
                self.display_final_variable.set(text)
        else:
            if text in self.arrow_keys:
                text = self.arrow_keys[text]
            if text in self.row4_mappings:
                text = self.row4_mappings[text]
            if text == "^(-1)":
                self.Cal.result += text
                self.Cal.convert_to_understandable()
                self.display_var.set(self.Cal.showing_exp)
                return
            self.fourier_solver.user_input(text)
            if text == "AC":
                self.display_var.set("Function to transform")
                return
            self.display_var.set(self.fourier_solver.showing_exp)

    def bind_keys(self):
        # Bind keyboard keys to the same function as button clicks
        self.bind_all("<KeyPress>", self.on_key_press)
        self.entry2.bind("<FocusIn>", lambda event: self.set_current_entry(self.entry2))
        self.entry3.bind("<FocusIn>", lambda event: self.set_current_entry(self.entry3))
        self.entry1.bind("<FocusIn>", lambda event: self.set_current_entry(self.entry1))

    def on_key_press(self, event):
        key = event.char
        if key:
            if self.current_entry == self.entry2:
                self.display_initial_variable.set(self.display_initial_variable.get() + key)
            elif self.current_entry == self.entry3:
                self.display_final_variable.set(self.display_final_variable.get() + key)
            else:
                self.display_var.set(self.display_var.get() + key)

    def set_current_entry(self, entry):
        self.current_entry = entry


class ShowFourierSpectrum(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="black")
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        # load image
        img = tk.PhotoImage(file='integrals/fourier_transform.png')
        label = tk.Label(self, image=img, borderwidth=0)
        label.image = img
        label.pack()

        close_button = tk.Button(self, text="Close", command=lambda: self.controller.show_frame("FourierTransform"))
        close_button.pack()

        show_button = tk.Button(self, text="Show Equation", command=lambda: self.controller.show_frame("ShowFourierSpectrum"))
        show_button.pack()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Fourier Transform Tool")
    frame = FourierTransform(root, None)
    frame.pack(fill="both", expand=True)
    root.mainloop()
