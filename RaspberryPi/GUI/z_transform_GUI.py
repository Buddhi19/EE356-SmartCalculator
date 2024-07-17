import tkinter as tk
from tkinter import ttk
import sympy as sp
import subprocess

class ZTransformCalculator(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#293C4A")
        self.controller = controller
        self.input_var = tk.StringVar()
        self.create_widgets()

    def create_widgets(self):
        # Display area
        input_entry = ttk.Entry(self, textvariable=self.input_var, font=('Arial', 20, 'bold'), justify='right')
        input_entry.grid(row=0, column=0, columnspan=6, sticky="nsew")

        # Button parameters
        button_params = {'fg': '#BBB', 'bg': '#3C3636', 'font': ('Arial', 11, 'bold'), 'width': 6, 'height': 2}
        special_params = {'fg': '#000', 'bg': '#db701f', 'font': ('Arial', 11, 'bold'), 'width': 6, 'height': 2}

        # Keypad
        buttons = [
            ['7', '8', '9', 'n', 'z', 'Z'],
            ['4', '5', '6', '+', '-', '*'],
            ['1', '2', '3', '/', '^', '('],
            ['0', '.', 'e', ')', 'DEL', 'AC'],
            ['sin', 'cos', 'tan', 'log', 'exp', '='],
            ['Back']
        ]

        for i, row in enumerate(buttons):
            for j, text in enumerate(row):
                if text in ['DEL', 'AC', '=', 'Back']:
                    b = tk.Button(self, text=text, command=lambda x=text: self.on_click(x), **special_params)
                else:
                    b = tk.Button(self, text=text, command=lambda x=text: self.on_click(x), **button_params)
                b.grid(row=i+2, column=j, sticky="nsew")

        for i in range(8):
            self.grid_rowconfigure(i, weight=1)
        for i in range(6):
            self.grid_columnconfigure(i, weight=1)

    def on_click(self, key):
        if key == '=':
            result = self.calculate_z_transform()
            print("Z-transform:", result)  # Print the result to console
            self.input_var.set('')  # Clear the input field
        elif key == 'AC':
            self.input_var.set('')
        elif key == 'DEL':
            current = self.input_var.get()
            self.input_var.set(current[:-1])
        elif key == 'Back':
            self.controller.destroy()
            subprocess.run(["python", "start2_gui.py"])
        else:
            current = self.input_var.get()
            self.input_var.set(current + key)

    def calculate_z_transform(self):
        try:
            expr = self.input_var.get()
            n = sp.Symbol('n')
            z = sp.Symbol('z')
            f = sp.sympify(expr)
            
            # Use Z-transform definition directly
            z_transform = sp.Sum(f * z**(-n), (n, 0, sp.oo))
            
            # Try to evaluate the sum
            z_transform_eval = z_transform.doit()
            
            if z_transform_eval != z_transform:
                # If we got a closed form
                return z_transform_eval
            else:
                # If closed form doesn't exist, calculate polynomial up to n^10
                series = sum(f.subs(n, k) * z**(-k) for k in range(11))
                return series
        except Exception as e:
            return f"Error: {str(e)}"

if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg="#293C4A")
    root.geometry("400x600")
    root.title("Z-Transform Calculator")

    calculator = ZTransformCalculator(root, root)
    calculator.pack(fill="both", expand=True)

    root.mainloop()
