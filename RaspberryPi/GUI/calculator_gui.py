import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main_controller import Calculator 
import tkinter as tk
from tkinter import ttk
import math

class Calculator_Frame(tk.Frame):
    def __init__(self,parent,controller):
        super().__init__(parent)
        self.controller = controller
        self.display_var = tk.StringVar()
        # self.wm_attributes("-fullscreen", "True")
        self.create_widgets()
        self.Cal = Calculator()
        self.MODE = "calculator"
        
    def create_widgets(self):
        entry = ttk.Entry(self, textvariable=self.display_var, font=('Arial', 20), justify='right', state='readonly')
        entry.grid(row=0, column=0, columnspan=8, sticky="nsew")
        
        buttons = [
            'left', 'right', '', 'MODE', 'DEL', 'AC', 'i',
            'x', 'y', 'z', 'x!', 'log',
            '7', '8', '9', '/', 'sin', 'cos', 'tan', 'hyp',
            '4', '5', '6', '*', 'ln', '(', ')', '√',
            '1', '2', '3', '-', '^', 'x⁻¹', 'pi', 'nCr',
            '0', '.', '±', '+', 'EXP', 'x10^x', '='
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

        back_button = ttk.Button(self, text="Back", command=lambda: self.controller.show_frame("StartPage"))
        back_button.grid(row=7, column=0, columnspan=8, sticky="nsew")
        
    def on_click(self, event):
        text = event.widget.cget("text")
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
    root.title("Standalone Calculator")
    
    # Initialize the Calculator frame
    calculator_frame = Calculator_Frame(root, root)
    calculator_frame.pack(fill="both", expand=True)
    
    root.mainloop()