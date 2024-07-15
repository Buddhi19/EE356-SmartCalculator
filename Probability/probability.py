import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from scipy import stats

class NormalDistributionCalculator(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.parent.title("Normal Distribution Calculator")
        
        # Set window size and colors
        window_width = 480
        window_height = 800
        self.parent.geometry(f"{window_width}x{window_height}")
        self.parent.resizable(False, False)
        self.parent.configure(bg='#3C3636')

        # Create custom styles with larger font
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background='#3C3636')
        style.configure('TLabel', background='#3C3636', foreground='#db701f', font=('TkDefaultFont', 12))
        style.configure('TEntry', fieldbackground='#3C3636', foreground='#db701f', font=('TkDefaultFont', 12))
        style.configure('TButton', background='#db701f', foreground='#3C3636', font=('TkDefaultFont', 12, 'bold'))
        style.map('TButton', background=[('active', '#db701f')])
        style.configure('TCombobox', fieldbackground='#3C3636', foreground='#3C3636', selectbackground='#db701f', font=('TkDefaultFont', 12))

        # Create main frame
        main_frame = ttk.Frame(self, padding="10")
        main_frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Create input fields
        ttk.Label(main_frame, text="Mean (μ):").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.mean_entry = ttk.Entry(main_frame, width=15)
        self.mean_entry.grid(row=0, column=1, padx=5, pady=5)
        self.mean_entry.insert(0, "0")

        ttk.Label(main_frame, text="Standard Deviation (σ):").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.std_entry = ttk.Entry(main_frame, width=15)
        self.std_entry.grid(row=1, column=1, padx=5, pady=5)
        self.std_entry.insert(0, "1")

        # Dropdown for selecting probability type
        self.prob_type = tk.StringVar(value="P(X > a)")
        ttk.Label(main_frame, text="Probability type:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.prob_type_dropdown = ttk.Combobox(main_frame, textvariable=self.prob_type, 
                                               values=("P(X > a)", "P(X < a)", "P(a < X < b)"), 
                                               state="readonly", width=15)
        self.prob_type_dropdown.grid(row=2, column=1, padx=5, pady=5)
        self.prob_type_dropdown.bind("<<ComboboxSelected>>", self.update_entry_fields)

        # Lower bound entry
        ttk.Label(main_frame, text="Lower bound (a):").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.lower_entry = ttk.Entry(main_frame, width=15)
        self.lower_entry.grid(row=3, column=1, padx=5, pady=5)
        self.lower_entry.insert(0, "1")

        # Upper bound entry (initially disabled)
        ttk.Label(main_frame, text="Upper bound (b):").grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        self.upper_entry = ttk.Entry(main_frame, width=15, state="disabled")
        self.upper_entry.grid(row=4, column=1, padx=5, pady=5)

        # Create calculate button
        self.calculate_button = ttk.Button(main_frame, text="Calculate", command=self.calculate)
        self.calculate_button.grid(row=5, column=0, columnspan=2, pady=10)

        # Create result label
        self.result_label = ttk.Label(main_frame, text="", font=('TkDefaultFont', 14, 'bold'))
        self.result_label.grid(row=6, column=0, columnspan=2, pady=5)

        # Create graph
        self.figure, self.ax = plt.subplots(figsize=(4.5, 4), facecolor='#3C3636')
        self.canvas = FigureCanvasTkAgg(self.figure, master=main_frame)
        self.canvas.get_tk_widget().grid(row=7, column=0, columnspan=2, padx=5, pady=5)

        self.update_graph()

    def update_entry_fields(self, event=None):
        if self.prob_type.get() == "P(a < X < b)":
            self.upper_entry.config(state="normal")
            self.upper_entry.delete(0, tk.END)
            self.upper_entry.insert(0, "2")
        else:
            self.upper_entry.config(state="disabled")

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
        self.ax.plot(x, y, color='#db701f')
        self.ax.set_facecolor('#3C3636')
        self.ax.set_title("Normal Distribution", color='#db701f', fontsize=14)
        self.ax.set_xlabel("X", color='#db701f', fontsize=12)
        self.ax.set_ylabel("Probability Density", color='#db701f', fontsize=12)
        self.ax.tick_params(colors='#db701f', labelsize=10)
        
        if prob_type == "P(X > a)":
            x_filled = np.linspace(lower, mean + 4*std, 100)
        elif prob_type == "P(X < a)":
            x_filled = np.linspace(mean - 4*std, lower, 100)
        else:  # "P(a < X < b)"
            upper = float(self.upper_entry.get())
            x_filled = np.linspace(lower, upper, 100)
        
        y_filled = stats.norm.pdf(x_filled, mean, std)
        self.ax.fill_between(x_filled, y_filled, color='#db701f', alpha=0.3)

        for spine in self.ax.spines.values():
            spine.set_edgecolor('#db701f')

        self.figure.tight_layout()
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = NormalDistributionCalculator(root)
    app.pack(fill="both", expand=True)
    root.mainloop()
