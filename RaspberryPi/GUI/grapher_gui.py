import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from grapher import Grapher # type: ignore
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt

class Graph_GUI(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.display_var = tk.StringVar()
        self.create_widgets()
        self.Graph = Grapher()

        # Style for ttk.Entry
        entry = ttk.Entry(self, textvariable=self.display_var, font=('sans-serif', 20, 'bold'), justify='right', state='readonly', style="Custom.TEntry")
        entry.grid(row=0, column=0, columnspan=8, padx=0, pady=15, sticky="nsew")
        
        # Set the background color of the frame to match the entry box
        self.configure(bg="#293C4A")

    def create_widgets(self):
        
        self.button_params = { 'fg': '#BBB', 'bg': '#3C3636', 'font': ('sans-serif', 15, 'bold')}
        self.button_params_main = {'bd': 5, 'fg': '#000', 'bg': '#BBB', 'font': ('sans-serif', 15, 'bold')}
        self.button_params_other = { 'fg': '#000', 'bg':'#db701f', 'font': ('sans-serif', 15, 'bold')}

        
        row1_buttons =['mode', '', '←', '→', '', '']
        row2_buttons =['x', 'y', 'z', 'log', '+', '-']
        row3_buttons =['sin', 'cos', 'tan', 'ln', '/', '*']
        row4_buttons =['7', '8', '9', '(', ')', 'hyp']
        row5_buttons =['4', '5', '6', '^',  'x⁻¹', '\u00B2\u221A']
        row6_buttons =['1', '2', '3', 'x10^x', 'π', '=']
        row7_buttons =['0', '.', 'EXP', 'plot','DEL' , 'AC']

        buttons_grid = [row1_buttons, row2_buttons, row3_buttons, row4_buttons, row5_buttons, row6_buttons,row7_buttons]

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
        if text == "plot":
            data = self.Graph.user_input(text)
            if data == "":
                self.display_var.set(self.Graph.showing_exp)
                return
            if "2D" in data:
                self.controller.show_frame("Graph_Frame2D", data["2D"])
            elif "3D" in data:
                self.controller.show_frame("Graph_Frame3D", data["3D"])
            return
        self.Graph.user_input(text)
        self.display_var.set(self.Graph.showing_exp)

class Graph_Frame2D(tk.Frame):
    def __init__(self, parent, controller, data):
        super().__init__(parent)
        self.controller = controller
        self.config(bg="black", width=600, height=800)
        self.x = data[0]
        self.y = data[1]
        self._create_widgets_2D()

    def _create_widgets_2D(self):
        frame = ttk.Frame(self)
        frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.fig = Figure(figsize=(5, 4), dpi=100, facecolor="black")
        self.ax = self.fig.add_subplot(111)
        
        self.ax.plot(self.x, self.y)

        self.ax.set_facecolor("black")
        self.ax.spines['bottom'].set_color('white')
        self.ax.spines['left'].set_color('white')
        self.ax.tick_params(axis='x', colors='white')
        self.ax.tick_params(axis='y', colors='white')
        self.ax.yaxis.label.set_color('white')
        self.ax.xaxis.label.set_color('white')

        self.canvas = FigureCanvasTkAgg(self.fig, master=frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        toolbar_frame = ttk.Frame(self)
        toolbar_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=False)
        toolbar = NavigationToolbar2Tk(self.canvas, toolbar_frame)
        toolbar.update()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.update_button = ttk.Button(self, text="Close", command=self.close)
        self.update_button.pack(side=tk.BOTTOM)

    def close(self):
        self.pack_forget()
        self.controller.show_frame("Graph_GUI")

class Graph_Frame3D(tk.Frame):
    def __init__(self, parent, controller, data):
        super().__init__(parent)
        self.controller = controller
        self.config(bg="black", width=600, height=800)
        self.x = data[0]    
        self.y = data[1]
        self.z = data[2]
        self._create_widgets_3D()

    def _create_widgets_3D(self):
        frame = ttk.Frame(self)
        frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.fig = plt.figure(figsize=(5, 4), dpi=100, facecolor="black")
        self.ax = self.fig.add_subplot(111, projection='3d')
        
        self.ax.plot_surface(self.x, self.y, self.z, cmap="viridis")

        self.ax.set_facecolor("black")
        self.ax.spines['bottom'].set_color('white')
        self.ax.spines['left'].set_color('white')
        self.ax.spines['right'].set_color('white')
        self.ax.spines['top'].set_color('white')
        self.ax.tick_params(axis='x', colors='white')
        self.ax.tick_params(axis='y', colors='white')
        self.ax.tick_params(axis='z', colors='white')
        self.ax.yaxis.label.set_color('white')
        self.ax.xaxis.label.set_color('white')
        self.ax.zaxis.label.set_color('white')
        self.ax.xaxis.pane.fill = False
        self.ax.yaxis.pane.fill = False
        self.ax.zaxis.pane.fill = False

        self.canvas = FigureCanvasTkAgg(self.fig, master=frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        plt.close()

        toolbar_frame = ttk.Frame(self)
        toolbar_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=False)
        toolbar = NavigationToolbar2Tk(self.canvas, toolbar_frame)
        toolbar.update()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.update_button = ttk.Button(self, text="Close", command=self.close)
        self.update_button.pack(side=tk.BOTTOM)

    def close(self):
        self.pack_forget()
        self.controller.show_frame("Graph_GUI")


if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg="#293C4A", bd=10)
    root.geometry("480x800")
    root.title("Standalone Calculator")

    # Initialize the Calculator frame
    calculator_frame = Graph_GUI(root, root)
    calculator_frame.pack(fill="both", expand=True)
    root.mainloop()