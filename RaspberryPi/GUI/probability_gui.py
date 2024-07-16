import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from scipy import stats

class NormalDistributionCalculator(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller
        
        self.parent.configure(bg='#343434')

        # Create custom styles with larger font
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background='#343434')
        style.configure('TLabel', background='#343434', foreground='#FFFFFF', font=('TkDefaultFont', 12))
        style.configure('TEntry', fieldbackground='#343434', foreground='#FFFFFF', font=('TkDefaultFont', 12))
        style.configure('TButton', background='#343434', foreground='#FFFFFF', font=('TkDefaultFont', 12, 'bold'))
        style.map('TButton', background=[('active', '#FF9500')])
        style.configure('TCombobox', fieldbackground='#343434', foreground='#FFFFFF', selectbackground='#FF9500', font=('TkDefaultFont', 12))

        # Create main frame
        main_frame = ttk.Frame(self, padding="10")
        main_frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Create graph (with reduced size)
        self.figure, self.ax = plt.subplots(figsize=(3.5, 3), facecolor='#3C3636')
        self.canvas = FigureCanvasTkAgg(self.figure, master=main_frame)
        self.canvas.get_tk_widget().grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        # Create input fields
        ttk.Label(main_frame, text="Mean (μ):").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.mean_entry = ttk.Entry(main_frame, width=15)
        self.mean_entry.grid(row=1, column=1, padx=5, pady=5)
        self.mean_entry.insert(0, "0")

        ttk.Label(main_frame, text="Standard Deviation (σ):").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.std_entry = ttk.Entry(main_frame, width=15)
        self.std_entry.grid(row=2, column=1, padx=5, pady=5)
        self.std_entry.insert(0, "1")

        # Dropdown for selecting probability type
        self.prob_type = tk.StringVar(value="P(X > a)")
        ttk.Label(main_frame, text="Probability type:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.prob_type_dropdown = ttk.Combobox(main_frame, textvariable=self.prob_type, 
                                               values=("P(X > a)", "P(X < a)", "P(a < X < b)"), 
                                               state="readonly", width=15)
        self.prob_type_dropdown.grid(row=3, column=1, padx=5, pady=5)
        self.prob_type_dropdown.bind("<<ComboboxSelected>>", self.update_entry_fields)

        # Lower bound entry
        ttk.Label(main_frame, text="Lower bound (a):").grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        self.lower_entry = ttk.Entry(main_frame, width=15)
        self.lower_entry.grid(row=4, column=1, padx=5, pady=5)
        self.lower_entry.insert(0, "1")

        # Upper bound entry (initially disabled)
        ttk.Label(main_frame, text="Upper bound (b):").grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)
        self.upper_entry = ttk.Entry(main_frame, width=15, state="disabled")
        self.upper_entry.grid(row=5, column=1, padx=5, pady=5)

        # Create keypad
        keypad_frame = ttk.Frame(main_frame)
        keypad_frame.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

        keypad_buttons = [
            '7', '8', '9',
            '4', '5', '6',
            '1', '2', '3',
            '0', '.', 'C'
        ]

        row, col = 0, 0
        for button in keypad_buttons:
            cmd = lambda x=button: self.keypad_click(x)
            ttk.Button(keypad_frame, text=button, command=cmd, width=5).grid(row=row, column=col, padx=2, pady=2)
            col += 1
            if col > 2:
                col = 0
                row += 1

        # Add buttons to select which field to input to
        field_buttons_frame = ttk.Frame(main_frame)
        field_buttons_frame.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

        field_buttons = [
            ("Mean (μ)", self.mean_entry),
            ("Std Dev (σ)", self.std_entry),
            ("Lower (a)", self.lower_entry),
            ("Upper (b)", self.upper_entry)
        ]

        for text, entry in field_buttons:
            cmd = lambda e=entry: self.set_active_entry(e)
            ttk.Button(field_buttons_frame, text=text, command=cmd, width=10).pack(side=tk.LEFT, padx=2)

        # Create calculate button
        self.calculate_button = ttk.Button(main_frame, text="Calculate", command=self.calculate)
        self.calculate_button.grid(row=8, column=0, columnspan=2, pady=10)

        # Create result label
        self.result_label = ttk.Label(main_frame, text="", font=('TkDefaultFont', 14, 'bold'))
        self.result_label.grid(row=9, column=0, columnspan=2, pady=5)

        # Create back button
        self.back_button = ttk.Button(main_frame, text="Back", command=self.go_back)
        self.back_button.grid(row=10, column=0, columnspan=2, pady=10)

        self.active_entry = self.mean_entry
        self.update_graph()

    def set_active_entry(self, entry):
        self.active_entry = entry
        if entry == self.upper_entry and self.prob_type.get() != "P(a < X < b)":
            self.prob_type.set("P(a < X < b)")
            self.update_entry_fields()

    def keypad_click(self, key):
        if key == 'C':
            self.active_entry.delete(0, tk.END)
        else:
            self.active_entry.insert(tk.END, key)

    def update_entry_fields(self, event=None):
        if self.prob_type.get() == "P(a < X < b)":
            self.upper_entry.config(state="normal")
            if not self.upper_entry.get():
                self.upper_entry.insert(0, "2")
        else:
            self.upper_entry.config(state="disabled")
            self.upper_entry.delete(0, tk.END)

    def calculate(self):
        try:
            mean = float(self.mean_entry.get())
            std = float(self.std_entry.get())
            lower = float(self.lower_entry.get())
            prob_type = self.prob_type.get()

            if prob_type == "P(X > a)":
                probability = 1 - stats.norm.cdf(lower, mean, std)
                result_text = f"P(X > {lower}) = {probability:.4f}"
            elif prob_type == "P(X < a)":
                probability = stats.norm.cdf(lower, mean, std)
                result_text = f"P(X < {lower}) = {probability:.4f}"
            else:  # "P(a < X < b)"
                upper = float(self.upper_entry.get())
                probability = stats.norm.cdf(upper, mean, std) - stats.norm.cdf(lower, mean, std)
                result_text = f"P({lower} < X < {upper}) = {probability:.4f}"

            self.result_label.config(text=result_text)
            self.update_graph()

        except ValueError:
            self.result_label.config(text="Invalid input. Please enter numeric values.")

    def update_graph(self):
        self.ax.clear()
        mean = float(self.mean_entry.get())
        std = float(self.std_entry.get())
        lower = float(self.lower_entry.get())
        prob_type = self.prob_type.get()

        x = np.linspace(mean - 4*std, mean + 4*std, 100)
        y = stats.norm.pdf(x, mean, std)
        self.ax.plot(x, y, color='#FF9500')
        self.ax.set_facecolor('#343434')
        self.ax.set_title("Normal Distribution", color='#FFFFFF', fontsize=12)
        self.ax.set_xlabel("X", color='#FFFFFF', fontsize=10)
        self.ax.set_ylabel("Probability Density", color='#FFFFFF', fontsize=10)
        self.ax.tick_params(colors='#FFFFFF', labelsize=8)
        
        if prob_type == "P(X > a)":
            x_filled = np.linspace(lower, mean + 4*std, 100)
        elif prob_type == "P(X < a)":
            x_filled = np.linspace(mean - 4*std, lower, 100)
        else:  # "P(a < X < b)"
            upper = float(self.upper_entry.get())
            x_filled = np.linspace(lower, upper, 100)
        
        y_filled = stats.norm.pdf(x_filled, mean, std)
        self.ax.fill_between(x_filled, y_filled, color='#FF9500', alpha=0.3)

        for spine in self.ax.spines.values():
            spine.set_edgecolor('#FFFFFF')

        self.figure.tight_layout()
        self.canvas.draw()

    def go_back(self):
        self.controller.show_frame("StartPage2")

if __name__ == "__main__":
    root = tk.Tk()
    app = NormalDistributionCalculator(root, None)
    app.pack(fill="both", expand=True)
    root.mainloop()