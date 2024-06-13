import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
from tkinter import ttk
from simultaneous_equations import Simul
from controls_solver import generate_bode_plot
from PIL import Image, ImageTk

class TransferFunctionFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="black")
        self.controller = controller
        
        self.numerator = "Transfer Function Numerator"
        self.denominator = "Transfer Function Denominator"

        # Create widgets
        self.create_widgets()

    def create_widgets(self):
        # Display the transfer function
        self.canvas = tk.Canvas(self, bg="black", highlightthickness=0, width=400, height=400)
        self.canvas.pack(pady=10)

        # Draw the fraction
        self.num = self.canvas.create_text(200, 50, text=self.numerator, fill="white", font=("Arial", 16), anchor="s")
        line =self.canvas.create_line(20, 60, 520, 60, fill="white", width=2)
        self.den = self.canvas.create_text(200, 80, text=self.denominator, fill="white", font=("Arial", 16), anchor="n")

        # Buttons
        self.button_frame = tk.Frame(self, bg="black")
        self.button_frame.pack(pady=10)


        self.edit_numerator_button = tk.Button(self.button_frame, text="Edit Numerator", command=self.edit_numerator, bg="black", fg="white")
        self.edit_numerator_button.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.edit_denominator_button = tk.Button(self.button_frame, text="Edit Denominator", command=self.edit_denominator, bg="black", fg="white")
        self.edit_denominator_button.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.bode_button = tk.Button(self.button_frame, text="Bode Plot", bg="black", fg="white",command=self.bode_plotter)
        self.bode_button.pack(side=tk.LEFT, fill=tk.X, expand=True)        

        self.root_locus_button = tk.Button(self.button_frame, text="Root Locus", bg="black", fg="white")
        self.root_locus_button.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.back_button = tk.Button(self.button_frame, text="Back", command=self.go_back, bg="black", fg="white")
        self.back_button.pack(side=tk.LEFT, fill=tk.X, expand=True)

    def edit_numerator(self):
        EditTransferFunction(self, self.update_numerator)
        
    def update_numerator(self, data):
        self.numerator = data
        self.canvas.delete(self.num)
        self.num = self.canvas.create_text(200, 50, text=self.numerator, fill="white", font=("Arial", 16), anchor="s", tag="numerator")

    def edit_denominator(self):
        EditTransferFunction(self, self.update_denominator)

    def update_denominator(self, data):
        self.denominator = data
        self.canvas.delete(self.den)
        self.den = self.canvas.create_text(200, 80, text=self.denominator, fill="white", font=("Arial", 16), anchor="n", tag="denominator")

    def go_back(self):
        self.controller.show_frame("StartPage")

    def bode_plotter(self):
        if self.numerator == "Transfer Function Numerator" or self.denominator == "Transfer Function Denominator":
            return
        generate_bode_plot(self.numerator, self.denominator)
        ShowPlots(self, "bode_plot")


class EditTransferFunction(tk.Toplevel):
    def __init__(self,parent,callback):
        super().__init__(parent)
        self.callback = callback
        self.display_var = tk.StringVar()
        self.solver = Simul()
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

        
        row1_buttons =['←', '→', '', '', 's', 'z']
        row3_buttons =['sin', 'cos', 'tan', 'ln', '(', ')']
        row4_buttons =['7', '8', '9', '/', '*', 'hyp']
        row5_buttons =['4', '5', '6', '^',  '+', '\u00B2\u221A']
        row6_buttons =['1', '2', '3','π','-', '=']
        row7_buttons =['0', '.', 'EXP','DEL' , 'AC']

        buttons_grid = [row1_buttons, row3_buttons, row4_buttons, row5_buttons, row6_buttons,row7_buttons]

        self.arrow_keys = { '←':"left", '→':"right"}
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

        back_button = tk.Button(self, text="Back", command=lambda: self.destroy(),**self.button_params_main)
        back_button.grid(row=8, column=0, columnspan=3, sticky="nsew")

        add_button = tk.Button(self, text="Add",**self.button_params_main)
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

    
class ShowPlots(tk.Toplevel):
    def __init__(self, parent, mode):
        super().__init__(parent)
        self.mode = mode
        self.create_widgets()

    def create_widgets(self):
        #show image named mode.png
        img = Image.open(f"{self.mode}.png")
        img = img.resize((480, 800))
        img = ImageTk.PhotoImage(img)
        panel = tk.Label(self, image=img)
        panel.image = img

        close_button = tk.Button(self, text="Close", command=self.destroy)
        panel.pack()
        close_button.pack()
        


if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg="black")
    root.geometry("330x800")
    transfer_function_frame = TransferFunctionFrame(root, None)
    transfer_function_frame.pack()
    root.mainloop()

