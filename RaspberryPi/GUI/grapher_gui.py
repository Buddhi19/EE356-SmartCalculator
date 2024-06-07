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
    def __init__(self,parent,controller):
        super().__init__(parent)
        self.controller = controller
        self.display_var = tk.StringVar()
        # self.wm_attributes("-fullscreen", "True")
        self.create_widgets()
        self.Graph = Grapher()
        
    def create_widgets(self):
        entry = ttk.Entry(self, textvariable=self.display_var, font=('Arial', 20), justify='right', state='readonly')
        entry.grid(row=0, column=0, columnspan=8, sticky="nsew")
        
        buttons = [
            'left', 'right', '', 'MODE', 'DEL', 'AC', '', '',
            'x', 'y', 'z', '∫', '∂', 'd/dx', 'x!', 'log',
            '7', '8', '9', '/', 'sin', 'cos', 'tan', 'hyp',
            '4', '5', '6', '*', 'ln', '(', ')', '√',
            '1', '2', '3', '-', 'x²', 'x⁻¹', 'pi', 'nCr',
            '0', '.', '±', '+', 'plot', 'EXP', 'x10^x', '='
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

    def on_click(self, event):
        text = event.widget.cget("text")
        if text == "plot":
            data = self.Graph.user_input(text)
            if data == "":
                self.display_var.set(self.Graph.showing_exp)
                return
            if "2D" in data:
                self.show_frame("Graph_Frame2D", data["2D"])
        self.Graph.user_input(text)
        self.display_var.set(self.Graph.showing_exp)

    def show_frame(self, name, data):
        if self.current_frame:
            self.frames[self.current_frame].grid_remove()
        self.current_frame = name
        self.frames[name].grid()

class Graph_Frame2D(tk.Frame):
    def __init__(self,parent,controller,data):
        super().__init__(parent)
        self.controller = controller
        self.config(bg="black",width=600,height=800)
        self.wm_attributes("-fullscreen", "True")
        self.x = data[0]
        self.y = data[1]
        self._create_widgets_2D()

    def _create_widgets_2D(self):
        # Create a frame for the plot and toolbar
        frame = ttk.Frame(self)
        frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Create a Matplotlib figure
        self.fig = Figure(figsize=(5, 4), dpi=100,facecolor="black")
        self.ax = self.fig.add_subplot(111)
        
        self.ax.plot(self.x,self.y)

        self.ax.set_facecolor("black")
        self.ax.spines['bottom'].set_color('white')
        self.ax.spines['left'].set_color('white')
        self.ax.tick_params(axis='x', colors='white')
        self.ax.tick_params(axis='y', colors='white')
        self.ax.yaxis.label.set_color('white')
        self.ax.xaxis.label.set_color('white')

        # Embed the Matplotlib figure in the Tkinter canvas
        self.canvas = FigureCanvasTkAgg(self.fig, master=frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Add the Matplotlib toolbar
        toolbar_frame = ttk.Frame(self)
        toolbar_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=False)
        toolbar = NavigationToolbar2Tk(self.canvas, toolbar_frame)
        toolbar.update()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Create a button to update the plot
        self.update_button = ttk.Button(self, text="Update Plot", command=self.change_plot)
        self.update_button.pack(side=tk.BOTTOM)

    def change_plot(self):
        # Update the plot with new data
        self.destroy()

    def close(self):
        self.destroy()

class Graph_Frame3D(tk.Frame):
    def __init__(self,parent,controller,data):
        super().__init__(parent)
        self.controller = controller
        self.config(bg="black",width=600,height=800)
        self.wm_attributes("-fullscreen", "True")
        self.x = data[0]    
        self.y = data[1]
        self.z = data[2]
        self._create_widgets_3D()

    def _create_widgets_3D(self):
        # Create a frame for the plot and toolbar
        frame = ttk.Frame(self)
        frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Create a Matplotlib figure
        self.fig = plt.figure(figsize=(5, 4), dpi=100, facecolor="black")
        self.ax = self.fig.add_subplot(111, projection='3d')
        
        self.ax.plot(self.x,self.y,self.z)

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

        # Embed the Matplotlib figure in the Tkinter canvas
        self.canvas = FigureCanvasTkAgg(self.fig, master=frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        plt.close()

        # Add the Matplotlib toolbar
        toolbar_frame = ttk.Frame(self)
        toolbar_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=False)
        toolbar = NavigationToolbar2Tk(self.canvas, toolbar_frame)
        toolbar.update()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Create a button to update the plot
        self.update_button = ttk.Button(self, text="Close", command=self.change_plot, width=10)
        self.update_button.pack(side=tk.BOTTOM)

    def change_plot(self):
        # Update the plot with new data
        self.destroy()



if __name__ == "__main__":
    root = tk.Tk()
    root.title("Standalone Calculator")

    # Initialize the Calculator frame
    calculator_frame = Graph_GUI(root, root)
    calculator_frame.pack(fill="both", expand=True)
    root.mainloop()