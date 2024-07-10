import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
from tkinter import ttk
from simultaneous_equations import Simul
from controls_solver import generate_bode_plot
from PIL import Image, ImageTk
import sympy as sp
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class TransferFunctionFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#293C4A")
        self.controller = controller
        self.configure(bg="#293C4A")
        
        self.numerator = "Transfer Function Numerator"
        self.denominator = "Transfer Function Denominator"

        # Create widgets
        self.create_widgets()

    def create_widgets(self):
        # Display the transfer function
        self.canvas = tk.Canvas(self, bg="#293C4A", highlightthickness=0)
        self.canvas.pack(expand=True,fill=tk.BOTH)

        # Draw the fraction
        self.num = self.canvas.create_text(170, 50, text=self.numerator, fill="white", font=('sans-serif', 12, 'bold'), anchor="s")
        line =self.canvas.create_line(30, 60, 300, 60, fill="white", width=2)
        self.den = self.canvas.create_text(170, 80, text=self.denominator, fill="white", font=('sans-serif', 12,'bold'), anchor="n")

        # Buttons
        self.button_frame = tk.Frame(self, bg="#293C4A")
        self.button_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=30)


        self.edit_numerator_button = tk.Button(self.button_frame, text="Edit Numerator" ,command=self.edit_numerator,font=('sans-serif', 10,'bold'), fg="#000",width=13)
        self.edit_numerator_button.grid(row=0, column=0, padx=5, pady=5)

        self.edit_denominator_button = tk.Button(self.button_frame, text="Edit Denominator", command=self.edit_denominator,font=('sans-serif', 10,'bold'), fg="#000",width=13)
        self.edit_denominator_button.grid(row=0, column=1, padx=5, pady=5)

        self.bode_button = tk.Button(self.button_frame, text="Bode Plot", command=self.bode_plotter, font=('sans-serif', 10,'bold'),fg="#000",width=13)
        self.bode_button.grid(row=1, column=0, padx=2, pady=5)        

        self.nyquist_button = tk.Button(self.button_frame, text="Nyquist Plot", command=self.nyquist_plotter, font=('sans-serif', 10,'bold'),fg="#000",width=13)
        self.nyquist_button.grid(row=1, column=1, padx=2, pady=5)

        self.back_button = tk.Button(self.button_frame, text="Back", command=self.go_back, font=('sans-serif', 10,'bold'),fg="#000",width=13)
        self.back_button.grid(row=2, column=1, padx=2, pady=5)

    def edit_numerator(self):
        EditTransferFunction(self, self.update_numerator)
        
    def update_numerator(self, data):
        self.numerator = data
        self.canvas.delete(self.num)
        self.num = self.canvas.create_text(170, 50, text=self.numerator, fill="white", font=('sans-serif', 16), anchor="s", tag="numerator")

    def edit_denominator(self):
        EditTransferFunction(self, self.update_denominator)

    def update_denominator(self, data):
        self.denominator = data
        self.canvas.delete(self.den)
        self.den = self.canvas.create_text(170, 80, text=self.denominator, fill="white", font=('sans-serif', 16), anchor="n", tag="denominator")

    def go_back(self):
        self.controller.show_frame("StartPage")

    def bode_plotter(self):
        if self.numerator == "Transfer Function Numerator" or self.denominator == "Transfer Function Denominator":
            return
        self.controller.show_frame("BODEplot", [self.numerator, self.denominator])

    def nyquist_plotter(self):
        if self.numerator == "Transfer Function Numerator" or self.denominator == "Transfer Function Denominator":
            return
        self.controller.show_frame("NyquistPlot", [self.numerator, self.denominator])


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
        
        self.button_params = { 'fg': '#BBB', 'bg': '#3C3636', 'font': ('sans-serif', 12, 'bold')}
        self.button_params_main = {'bd': 5, 'fg': '#000', 'bg': '#BBB', 'font': ('sans-serif', 12, 'bold')}
        self.button_params_other = { 'fg': '#000', 'bg':'#db701f', 'font': ('sans-serif', 12, 'bold')}

        
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
        
class BODEplot(tk.Frame):
    def __init__(self, parent, controller,data):
        super().__init__(parent)
        self.controller = controller
        self.config(bg="black", width=480, height=800)
        self.numerator = self.convert_to_array(data[0])
        self.denominator = self.convert_to_array(data[1])

        self.create_widgets()

    def convert_to_array(self, string):
        s = sp.symbols("s")
        poly = sp.Poly(string, s)
        coefficients = poly.all_coeffs()
        coefficients = [float(coef) for coef in coefficients]
        return coefficients
        
    def create_widgets(self):
        self.system = signal.TransferFunction(self.numerator, self.denominator)

        w, mag, phase = signal.bode(self.system)

        plot_frame = ttk.Frame(self,style="TFrame")
        plot_frame.grid(row=0, column=0, sticky="nw")

        self.fig, (self.ax_mag, self.ax_phase) = plt.subplots(2, 1, figsize=(4.7, 7), dpi=100, facecolor="black")

        # Configure magnitude subplot
        self.ax_mag.plot(w, mag, color='white')
        self.ax_mag.set_xscale('log')
        self.ax_mag.set_title('Bode Plot', color='white')
        self.ax_mag.set_ylabel('Magnitude (dB)', color='white')
        self.ax_mag.set_facecolor("black")
        self.ax_mag.spines['bottom'].set_color('white')
        self.ax_mag.spines['left'].set_color('white')
        self.ax_mag.tick_params(axis='x', colors='white')
        self.ax_mag.tick_params(axis='y', colors='white')
        self.ax_mag.yaxis.label.set_color('white')

        # Configure phase subplot
        self.ax_phase.plot(w, phase, color='white')
        self.ax_phase.set_xscale('log')
        self.ax_phase.set_ylabel('Phase (degrees)', color='white')
        self.ax_phase.set_xlabel('Frequency (rad/s)', color='white')
        self.ax_phase.set_facecolor("black")
        self.ax_phase.spines['bottom'].set_color('white')
        self.ax_phase.spines['left'].set_color('white')
        self.ax_phase.tick_params(axis='x', colors='white')
        self.ax_phase.tick_params(axis='y', colors='white')
        self.ax_phase.yaxis.label.set_color('white')
        self.ax_phase.xaxis.label.set_color('white')

        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nw")

        self.close_button = ttk.Button(self, text="Close", command=self.close)
        self.close_button.grid(row=3, column=0, pady=10, sticky="nw")

    def close(self):
        self.pack_forget()
        self.controller.show_frame("TransferFunctionFrame")

class NyquistPlot(tk.Frame):
    def __init__(self, parent, controller, data):
        super().__init__(parent)
        self.controller = controller
        self.config(bg="black", width=480, height=800)
        self.numerator = self.convert_to_array(data[0])
        self.denominator = self.convert_to_array(data[1])

        self.create_widgets()

    def convert_to_array(self, string):
        s = sp.symbols("s")
        poly = sp.Poly(string, s)
        coefficients = poly.all_coeffs()
        coefficients = [float(coef) for coef in coefficients]
        return coefficients

    def create_widgets(self):
        self.system = signal.TransferFunction(self.numerator, self.denominator)

        # Calculate Nyquist plot
        w, H = signal.freqresp(self.system)

        plot_frame = ttk.Frame(self, style="TFrame")
        plot_frame.grid(row=0, column=0, sticky="nw")

        # Create figure for Nyquist plot
        self.fig = plt.Figure(figsize=(4.5, 7), dpi=100, facecolor="black")
        self.ax = self.fig.add_subplot(111)

        # Plot Nyquist plot
        self.ax.plot(H.real, H.imag, 'white')
        self.ax.plot(H.real, -H.imag, 'white')
        self.ax.set_title('Nyquist Plot', color='white')
        self.ax.set_xlabel('Real', color='white')
        self.ax.set_ylabel('Imaginary', color='white')
        self.ax.set_facecolor("black")
        self.ax.spines['bottom'].set_color('white')
        self.ax.spines['left'].set_color('white')
        self.ax.tick_params(axis='x', colors='white')
        self.ax.tick_params(axis='y', colors='white')
        self.ax.xaxis.label.set_color('white')
        self.ax.yaxis.label.set_color('white')

        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nw")

        self.close_button = ttk.Button(self, text="Close", command=self.close)
        self.close_button.grid(row=1, column=0, pady=10, sticky="nw")

    def close(self):
        self.pack_forget()
        self.controller.show_frame("TransferFunctionFrame")


if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg="#293C4A")
    root.geometry("330x800")
    transfer_function_frame = TransferFunctionFrame(root, None)
    transfer_function_frame.pack()
    root.mainloop()

