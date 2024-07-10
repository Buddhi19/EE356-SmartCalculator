import tkinter as tk
from tkinter import messagebox

class DiscreteSignalCalculator(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        
        self.controller = controller
        self.current_input = ""
        self.signal = []

        self.create_widgets()

    def create_widgets(self):
        # Display area
        self.display = tk.Text(self, height=4, width=30, font=('Arial', 18))
        self.display.grid(row=0, column=0, columnspan=4, padx=5, pady=5, sticky="nsew")

        # Signal display
        self.signal_display = tk.Text(self, height=10, width=30, font=('Arial', 14))
        self.signal_display.grid(row=1, column=0, columnspan=4, padx=5, pady=5, sticky="nsew")

        # Buttons
        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', 'n', '+'
        ]

        row = 2
        col = 0
        for button in buttons:
            cmd = lambda x=button: self.click(x)
            tk.Button(self, text=button, command=cmd, width=5, height=2, font=('Arial', 18)).grid(row=row, column=col, sticky="nsew", padx=2, pady=2)
            col += 1
            if col > 3:
                col = 0
                row += 1

        # Additional buttons
        tk.Button(self, text="C", command=self.clear, width=5, height=2, font=('Arial', 18)).grid(row=row, column=0, sticky="nsew", padx=2, pady=2)
        tk.Button(self, text="^", command=lambda: self.click('^'), width=5, height=2, font=('Arial', 18)).grid(row=row, column=1, sticky="nsew", padx=2, pady=2)
        tk.Button(self, text="Add", command=self.add_to_signal, width=5, height=2, font=('Arial', 18)).grid(row=row, column=2, columnspan=2, sticky="nsew", padx=2, pady=2)

        # Configure grid
        for i in range(6):
            self.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.grid_columnconfigure(i, weight=1)

    def click(self, key):
        if key == 'n':
            if self.current_input and self.current_input[-1].isdigit():
                self.current_input += '*n'
            else:
                self.current_input += 'n'
        elif key == '^':
            if self.current_input and self.current_input[-1] in ('n', ')', ']', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
                self.current_input += '^'
            else:
                messagebox.showerror("Error", "^ must follow n or a number")
        else:
            self.current_input += str(key)
        self.update_display()

    def clear(self):
        self.current_input = ""
        self.update_display()

    def update_display(self):
        self.display.delete(1.0, tk.END)
        self.display.insert(tk.END, self.current_input)

    def add_to_signal(self):
        if 'n' in self.current_input:
            self.signal.append(self.current_input)
            self.update_signal_display()
            self.current_input = ""
            self.update_display()
        else:
            messagebox.showerror("Error", "Input must contain 'n'")

    def update_signal_display(self):
        self.signal_display.delete(1.0, tk.END)
        for item in self.signal:
            self.signal_display.insert(tk.END, f"x[n] = {item}\n")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Discrete Signal Calculator")
    root.geometry("480x800")
    
    calculator = DiscreteSignalCalculator(root, root)
    calculator.pack(expand=True, fill=tk.BOTH)
    
    root.mainloop()