import tkinter as tk
from tkinter import ttk

#plot bode plot when transfer function is given with matplotlib backend
import numpy as np
from scipy import signal
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt


class Controls_GUI(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
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

        
        row1_buttons =['', '', '←', '→', '', '']
        row2_buttons =['s', 'z', '', '', '+', '-']
        row4_buttons =['7', '8', '9', '(', ')', '']
        row5_buttons =['4', '5', '6', '^',  '*', '/']
        row6_buttons =['1', '2', '3', '', 'π', '=']
        row7_buttons =['0', '.', 'EXP', 'BodePlot','DEL' , 'AC']

        buttons_grid = [row1_buttons, row2_buttons, row4_buttons, row5_buttons, row6_buttons,row7_buttons]

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

        back_button = tk.Button(self, text="Back", command=lambda: self.controller.show_frame("StartPage"), **self.button_params_main)
        back_button.grid(row=8, column=0, columnspan=6, sticky="nsew")

    def on_click(self, event):
        text = event.widget.cget("text") 
        self.display_var.set(self.display_var.get() + text)



class BodePlot(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()
        self.bode_plot()

    def create_widgets(self):
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        back_button = tk.Button(self, text="Back", command=self.back)
        back_button.pack(side=tk.BOTTOM)

    def bode_plot(self):
        num = [1]
        den = [1, 1]
        system = signal.TransferFunction(num, den)
        w, mag, phase = signal.bode(system)
        self.ax.semilogx(w, mag)
        self.ax.set_title("Bode Plot")
        self.ax.set_xlabel("Frequency")
        self.ax.set_ylabel("Magnitude")
        self.canvas.draw()

    def back(self):
        self.controller.show_frame("StartPage")


if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg="#293C4A", bd=10)
    root.geometry("480x800")
    app = Controls_GUI(root, root)
    app.pack(fill="both", expand=True)
    app.mainloop()