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
        entry = ttk.Entry(self, textvariable=self.display_var, font=('sans-serif', 20, 'bold'), justify='right', state='readonly')
        entry.grid(row=0, column=0, columnspan=9, pady=20, sticky="nsew")
        # Set the background color of the frame to match the entry box     
        self.configure(bg="#293C4A")

    def create_widgets(self):
        self.button_params = { 'fg': '#BBB', 'bg': '#3C3636', 'font': ('sans-serif', 11, 'bold')}
        self.button_params_main = {'bd': 5, 'fg': '#000', 'bg': '#BBB', 'font': ('sans-serif', 11, 'bold')}
        self.button_params_other = { 'fg': '#000', 'bg':'#db701f', 'font': ('sans-serif', 11, 'bold')}

        row1_buttons = ['shift', 'MODE', '', '↑','', 'ln']
        row1_shift_buttons = ['sin⁻¹', 'cos⁻¹', 'tan⁻¹']
        row2_buttons = ['pi', 'pi', '←', '', '→', 'log']
        row3_buttons = ['x', 'y', 'z', '↓', '(', ')']
        row4_buttons = ['7', '8', '9', 'tan', 'sin', 'cos']
        row5_buttons = ['4', '5', '6', '+', '-',"AC"]
        row6_buttons = ['1', '2', '3', "*","/", 'DEL']
        row7_buttons = ['0', '.', 'EXP', 'x\u207b\xb9', '=','plot']

        buttons_grid = [row1_buttons, row2_buttons, row3_buttons, row4_buttons, row5_buttons, row6_buttons, row7_buttons]

        self.arrow_keys = {'↑':"up", '↓':"down", '←':"left", '→':"right"}
        special_buttons = {'DEL', 'AC', '='}

        row = 2
        for row_buttons in buttons_grid:
            col = 0
            for button in row_buttons:
                if button in self.arrow_keys:
                    b = tk.Button(self, text=button, **self.button_params_main, width=4,height=3)
                elif button in special_buttons:
                    b = tk.Button(self, text=button, **self.button_params_other, width=4,height=3)
                else:
                    b = tk.Button(self, text=button, **self.button_params, width=4,height=3)
                

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

        back_button = tk.Button(self, text="Back", command=lambda: self.controller.show_frame("StartPage"), **self.button_params_main,height=2,pady=10)
        back_button.grid(row=9, column=0, columnspan=7, sticky="nsew")         

    def on_click(self, event):
        text = event.widget.cget("text")
        if text in self.arrow_keys:
            text = self.arrow_keys[text]
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
        self.config(bg="black", width=480, height=800)
        self.x = data[0]
        self.y = data[1]
        self._create_widgets_2D()

    def _create_widgets_2D(self):
        # Frame for the plot and toolbar
        plot_frame = ttk.Frame(self, style="TFrame")
        plot_frame.grid(row=0, column=0, sticky="nw")

        # Create the figure
        self.fig = Figure(figsize=(4.3, 6), dpi=100, facecolor="black")
        self.ax = self.fig.add_subplot(111)
        
        self.ax.plot(self.x, self.y)
        self.ax.set_facecolor("black")
        self.ax.spines['bottom'].set_color('white')
        self.ax.spines['left'].set_color('white')
        self.ax.tick_params(axis='x', colors='white')
        self.ax.tick_params(axis='y', colors='white')
        self.ax.yaxis.label.set_color('white')
        self.ax.xaxis.label.set_color('white')

        # Create the canvas
        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nw")

        # Toolbar frame
        toolbar_frame = ttk.Frame(self, style="TFrame")
        toolbar_frame.grid(row=1, column=0, sticky="nw")
        toolbar = NavigationToolbar2Tk(self.canvas, toolbar_frame)
        toolbar.update()

        # Additional controls frame
        controls_frame = ttk.Frame(self, style="TFrame")
        controls_frame.grid(row=2, column=0, sticky="nw")
        # Add other controls here if needed

        # Close button
        self.update_button = ttk.Button(self, text="Close", command=self.close)
        self.update_button.grid(row=3, column=0, pady=10, sticky="nw")

    def close(self):
        self.pack_forget()
        self.controller.show_frame("Graph_GUI")



class Graph_Frame3D(tk.Frame):
    def __init__(self, parent, controller, data):
        super().__init__(parent)
        self.controller = controller
        self.config(bg="black", width=480, height=800)
        self.x = data[0]    
        self.y = data[1]
        self.z = data[2]
        self._create_widgets_3D()

    def _create_widgets_3D(self):
        # Create the figure and the 3D plot
        self.fig = plt.figure(figsize=(4.3, 6), dpi=100, facecolor="black")
        self.ax = self.fig.add_subplot(111, projection='3d')
        
        self.ax.plot_surface(self.x, self.y, self.z, cmap="viridis")

        self.ax.set_facecolor("black")
        self.ax.tick_params(axis='x', colors='white')
        self.ax.tick_params(axis='y', colors='white')
        self.ax.tick_params(axis='z', colors='white')
        self.ax.yaxis.label.set_color('white')
        self.ax.xaxis.label.set_color('white')
        self.ax.zaxis.label.set_color('white')
        self.ax.xaxis.pane.fill = False
        self.ax.yaxis.pane.fill = False
        self.ax.zaxis.pane.fill = False

        # Create the canvas to display the plot
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0, padx=10, pady=10, sticky="nw")

        # Toolbar below the plot
        toolbar_frame = ttk.Frame(self)
        toolbar_frame.grid(row=1, column=0, padx=10, pady=5, sticky="nw")
        toolbar = NavigationToolbar2Tk(self.canvas, toolbar_frame)
        toolbar.update()

        # Frame for control buttons
        control_frame = ttk.Frame(self)
        control_frame.grid(row=2, column=0, padx=10, pady=5, sticky="nw")

        # Close button at the bottom
        self.close_button = ttk.Button(self, text="Close", command=self.close)
        self.close_button.grid(row=3, column=0, padx=10, pady=10, sticky="se")

    def example_action(self):
        print("Example button clicked!")

    def close(self):
        self.pack_forget()
        self.controller.show_frame("Graph_GUI")


if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg="#293C4A", bd=10)
    root.geometry("330x800")
    root.title("Standalone Calculator")

    # Initialize the Calculator frame
    calculator_frame = Graph_GUI(root, root)
    calculator_frame.pack(fill="both", expand=True)
    root.mainloop()