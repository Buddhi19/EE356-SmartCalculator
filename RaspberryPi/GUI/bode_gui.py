import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy import signal
import control 
from control import tf, root_locus, nyquist_plot, bode_plot

def draw_nyquist_plot(numerator, denominator):
    # Create the transfer function
    system = tf(numerator, denominator)

    # Plot the Nyquist plot
    plt.figure(figsize=(3.3, 8))  # Set size to 330x800 pixels
    nyquist_plot(system)
    plt.title('Nyquist Plot')
    plt.xlabel('Real Axis')
    plt.ylabel('Imaginary Axis')
    plt.grid(True)
    plt.show()

# def draw_bode_plot(numerator, denominator):
#     # Create the transfer function
#     system = tf(numerator, denominator)

#     # Plot the Bode plot
#     fig = plt.figure(figsize=(3.3, 8))  # Set size to 330x800 pixels
#     mag, phase, omega = bode_plot(system, Plot=False)  # Plot=False to suppress automatic plot display
#     plt.title('Bode Plot')
    
#     plt.show()

def draw_bode_plot(numerator,denominator):
    transfer_function = signal.TransferFunction(numerator, denominator)
    w, mag, phase = signal.bode(transfer_function)

    #plot in black background name axis and title for both plots
    fig, ax = plt.subplots(2, 1, figsize=(3.3, 8))
    ax[0].plot(w, mag)
    ax[0].set_xscale('log')
    ax[0].set_title('Magnitude Plot')
    ax[0].set_ylabel('Magnitude (dB)')
    ax[0].set_xlabel('Frequency (rad/s)')
    ax[0].grid()

    ax[1].plot(w, phase)
    ax[1].set_xscale('log')
    ax[1].set_title('Phase Plot')
    ax[1].set_ylabel('Phase (degrees)')
    ax[1].set_xlabel('Frequency (rad/s)')
    ax[1].grid()
    plt.show()

def transfer_function_visual(num_coeffs, den_coeffs):
    num_len = len(num_coeffs)
    den_len = len(den_coeffs)
    num_poly = ""
    den_poly = ""
    for i in range(num_len):
        num_poly += str(num_coeffs[i])+"s^"+str(num_len-(i+1))+" + " if i != (num_len-1) else str(num_coeffs[i])

    for i in range(den_len):
        den_poly += str(den_coeffs[i])+"s^"+str(den_len-(i+1)) + " + " if i != (den_len-1) else str(den_coeffs[i])
    return num_poly, den_poly

class PlotApp(tk.Frame):
    def __init__(self, parent, controller, num_coeffs, den_coeffs):
        super().__init__(parent)
        self.controller = controller
        self.num_coeffs = num_coeffs
        self.den_coeffs = den_coeffs

        self.create_widgets()

    def create_widgets(self):
        num, den = transfer_function_visual(self.num_coeffs, self.den_coeffs)

        # Label for transfer function (optional)
        ttk.Label(self, text="Transfer Function:").grid(row=0, column=0, columnspan=2, padx=5, pady=5)
        ttk.Label(self, text=f"Numerator: {num}").grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        ttk.Label(self, text=f"Denominator: {den}").grid(row=2, column=0, columnspan=2, padx=10, pady=5)

        # Option menu for plot selection
        ttk.Label(self, text="Select plot type:").grid(row=3, column=0, padx=10, pady=5)
        self.plot_type_var = tk.StringVar()
        self.plot_type_var.set("Bode Plot")  # Default option
        plot_options = ["Bode Plot", "Nyquist Plot", "Root Locus Plot"]
        option_menu = ttk.OptionMenu(self, self.plot_type_var, self.plot_type_var.get(), *plot_options)
        option_menu.grid(row=3, column=1, padx=10, pady=5)

        # Button to plot selected plot type
        ttk.Button(self, text="Plot", command=self.plot_selected).grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        # Canvas for displaying plots
        self.canvas_frame = ttk.Frame(self)
        self.canvas_frame.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

    def plot_selected(self):
        plot_type = self.plot_type_var.get()

        if plot_type == "Bode Plot":
            self.plot_bode()
        elif plot_type == "Nyquist Plot":
            self.plot_nyquist()
        elif plot_type == "Root Locus Plot":
            self.plot_root_locus()

    def plot_bode(self):
        # Use the provided draw_bode_plot function
        draw_bode_plot(self.num_coeffs, self.den_coeffs)

    def plot_nyquist(self):
        # Use the provided draw_nyquist_plot function
        draw_nyquist_plot(self.num_coeffs, self.den_coeffs)

    def plot_root_locus(self):
        # Create the transfer function from coefficients
        sys = signal.TransferFunction(self.num_coeffs, self.den_coeffs)

        # Plot the root locus
        plt.figure(figsize=(3.3, 8))  # Set size to 330x800 pixels
        control.root_locus(sys)
        plt.title('Root Locus')
        plt.xlabel('Real Axis')
        plt.ylabel('Imaginary Axis')
        plt.grid(True)

        # Display plot in tkinter window (optional)
        plt.show()

    def display_plot(self, fig):
        # Clear previous plot
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

        # Display plot in tkinter window
        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

class PlotController(tk.Tk):
    def __init__(self, num_coeffs, den_coeffs, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Transfer Function Plots Controller")
        self.geometry("330x800")  # Adjust window size to 330x800 pixels

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Show PlotApp with provided coefficients
        frame = PlotApp(container, self, num_coeffs, den_coeffs)
        frame.grid(row=0, column=0, sticky="nsew")

if __name__ == "__main__":
    # Define the transfer function coefficients here
    num_coeffs = [2,1]
    den_coeffs = [1, 3, 3, 5]

    # Create the application
    app = PlotController(num_coeffs, den_coeffs)
    app.mainloop()