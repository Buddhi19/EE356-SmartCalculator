import tkinter as tk
from tkinter import ttk
import numpy as np

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Matrix Solver")
        self.geometry("800x600")
        self.frames = {}

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.add_frame(MatrixOperationPage)

    def add_frame(self, frame_class, data=None):
        if data:
            frame = frame_class(self.container, self, data)
        else:
            frame = frame_class(self.container, self)
        self.frames[frame_class.__name__] = frame
        frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, name, data=None):
        print(f"Switching to frame: {name}")
        if self.current_frame:
            self.frames[self.current_frame].grid_remove()
        if data:
            frame_class = globals()[name]
            frame = frame_class(self.container, self, data)
            self.frames[name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        else:
            frame_class = globals()[name]
            frame = frame_class(self.container, self)
            self.frames[name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.current_frame = name
        self.frames[name].grid()
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

class MatrixInputPage(tk.Toplevel):
    def __init__(self, parent, callback):
        super().__init__(parent)
        self.callback = callback
        self.configure(bg="#293C4A")

        label = tk.Label(self, text="Enter Matrix Dimensions", font=('sans-serif', 24, 'bold'), bg="#293C4A", fg="#BBB")
        label.pack(pady=20)

        self.row_var = tk.IntVar(value=2)
        self.col_var = tk.IntVar(value=2)

        row_label = tk.Label(self, text="Rows:", font=('sans-serif', 15, 'bold'), bg="#293C4A", fg="#BBB")
        row_label.pack(pady=5)
        self.row_menu = ttk.Combobox(self, textvariable=self.row_var, values=[2, 3, 4, 5], font=('sans-serif', 15, 'bold'))
        self.row_menu.pack(pady=5)

        col_label = tk.Label(self, text="Columns:", font=('sans-serif', 15, 'bold'), bg="#293C4A", fg="#BBB")
        col_label.pack(pady=5)
        self.col_menu = ttk.Combobox(self, textvariable=self.col_var, values=[2, 3, 4, 5], font=('sans-serif', 15, 'bold'))
        self.col_menu.pack(pady=5)

        self.matrix_var = tk.StringVar(value='MatA')
        matrix_label = tk.Label(self, text="Select Matrix:", font=('sans-serif', 15, 'bold'), bg="#293C4A", fg="#BBB")
        matrix_label.pack(pady=5)
        self.matrix_menu = ttk.Combobox(self, textvariable=self.matrix_var, values=['MatA', 'MatB', 'MatC', 'MatD', 'MatE'], font=('sans-serif', 15, 'bold'))
        self.matrix_menu.pack(pady=5)

        button = tk.Button(self, text="Next", command=self.next_page,
                           font=('sans-serif', 15, 'bold'), bg="#BBB", fg="#000")
        button.pack(pady=20)

    def next_page(self):
        rows = self.row_var.get()
        cols = self.col_var.get()
        matrix_name = self.matrix_var.get()
        self.callback(rows, cols, matrix_name)
        self.destroy()

class MatrixEntryPage(tk.Toplevel):
    def __init__(self, parent, callback):
        super().__init__(parent)
        self.callback = callback
        self.configure(bg="#293C4A")

        self.label = tk.Label(self, text="Enter Matrix Values", font=('sans-serif', 24, 'bold'), bg="#293C4A", fg="#BBB")
        self.label.pack(pady=20)

        self.matrix_frame = tk.Frame(self, bg="#293C4A")
        self.matrix_frame.pack()

        self.num_pad_frame = tk.Frame(self, bg="#293C4A")
        self.num_pad_frame.pack()

        self.num_pad = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2),
            ('0', 4, 1), ('.', 4, 0), ('-', 4, 2)
        ]

        self.entries = []

        for (text, row, col) in self.num_pad:
            button = tk.Button(self.num_pad_frame, text=text, command=lambda t=text: self.num_pad_click(t),
                               font=('sans-serif', 15, 'bold'), bg="#BBB", fg="#000", width=5)
            button.grid(row=row, column=col)

        self.current_entry = None

        self.add_button = tk.Button(self, text="Add Matrix", command=self.add_matrix,
                                    font=('sans-serif', 15, 'bold'), bg="#BBB", fg="#000")
        self.add_button.pack(pady=20)

        back_button = tk.Button(self, text="Back", command=lambda: self.destroy(),
                                font=('sans-serif', 15, 'bold'), bg="#BBB", fg="#000")
        back_button.pack(pady=10)

    def set_matrix_details(self, rows, cols, matrix_name):
        self.rows = rows
        self.cols = cols
        self.matrix_name = matrix_name
        self.create_matrix_entries()

    def create_matrix_entries(self):
        for widget in self.matrix_frame.winfo_children():
            widget.destroy()
        self.entries = []

        for r in range(self.rows):
            row_entries = []
            for c in range(self.cols):
                entry = tk.Entry(self.matrix_frame, font=('sans-serif', 15, 'bold'), width=5)
                entry.grid(row=r, column=c, padx=5, pady=5)
                entry.bind("<FocusIn>", self.set_current_entry)
                row_entries.append(entry)
            self.entries.append(row_entries)

    def set_current_entry(self, event):
        self.current_entry = event.widget

    def num_pad_click(self, value):
        if self.current_entry is not None:
            current_text = self.current_entry.get()
            if value == 'DEL':
                self.current_entry.delete(len(current_text) - 1)
            elif value == 'CLR':
                self.current_entry.delete(0, tk.END)
            else:
                self.current_entry.insert(tk.END, value)

    def add_matrix(self):
        matrix = []
        for row_entries in self.entries:
            row = [float(entry.get()) for entry in row_entries]
            matrix.append(row)
        self.callback(self.matrix_name, np.array(matrix))
        self.destroy()

class MatrixOperationPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="#293C4A")

        self.matrices = {name: None for name in ['MatA', 'MatB', 'MatC', 'MatD', 'MatE']}

        self.label = tk.Label(self, text="Matrix Operations", font=('sans-serif', 24, 'bold'), bg="#293C4A", fg="#BBB")
        self.label.pack(pady=20)

        self.operation_entry = tk.Entry(self, font=('sans-serif', 15, 'bold'), bg="#BBB", fg="#000", justify='right')
        self.operation_entry.pack(pady=10)

        self.result_label = tk.Label(self, text="", font=('sans-serif', 15, 'bold'), bg="#293C4A", fg="#BBB")
        self.result_label.pack(pady=10)

        self.operation_pad_frame = tk.Frame(self, bg="#293C4A")
        self.operation_pad_frame.pack(pady=10)

        operations = ['+', '-', '*', 'inv', '=', 'DEL', 'AC']
        self.operation_buttons = []
        for op in operations:
            button = tk.Button(self.operation_pad_frame, text=op, command=lambda o=op: self.perform_operation(o),
                               font=('sans-serif', 15, 'bold'), bg="#BBB", fg="#000", width=5)
            button.grid(row=0, column=operations.index(op), padx=5, pady=5)
            self.operation_buttons.append(button)

        self.matrix_buttons_frame = tk.Frame(self, bg="#293C4A")
        self.matrix_buttons_frame.pack(pady=20)

        self.num_pad_frame = tk.Frame(self, bg="#293C4A")
        self.num_pad_frame.pack(pady=20)

        self.num_pad = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2),
            ('0', 4, 1), ('.', 4, 0), ('-', 4, 2)
        ]

        for (text, row, col) in self.num_pad:
            button = tk.Button(self.num_pad_frame, text=text, command=lambda t=text: self.num_pad_click(t),
                               font=('sans-serif', 15, 'bold'), bg="#BBB", fg="#000", width=5)
            button.grid(row=row, column=col)

        add_matrix_button = tk.Button(self, text="Add Matrix", command=self.add_matrix,
                                      font=('sans-serif', 15, 'bold'), bg="#BBB", fg="#000")
        add_matrix_button.pack(pady=20)

        back_button = tk.Button(self, text="Back", command=lambda: controller.show_frame("MatrixInputPage"),
                                font=('sans-serif', 15, 'bold'), bg="#BBB", fg="#000")
        back_button.pack(pady=10)

        self.update_matrix_buttons()

    def update_matrix_buttons(self):
        for widget in self.matrix_buttons_frame.winfo_children():
            widget.destroy()

        for name in self.matrices.keys():
            button = tk.Button(self.matrix_buttons_frame, text=name, command=lambda n=name: self.set_matrix(n),
                               font=('sans-serif', 15, 'bold'), bg="#BBB", fg="#000", width=5)
            button.pack(side=tk.LEFT, padx=5)

    def add_matrix(self):
        self.matrix_input_page = MatrixInputPage(self, self.open_matrix_entry_page)

    def open_matrix_entry_page(self, rows, cols, matrix_name):
        self.matrix_entry_page = MatrixEntryPage(self, self.store_matrix)
        self.matrix_entry_page.set_matrix_details(rows, cols, matrix_name)

    def store_matrix(self, name, matrix):
        self.matrices[name] = matrix
        self.update_matrix_buttons()
        self.controller.show_frame("MatrixOperationPage")

    def set_matrix(self, name):
        current_text = self.operation_entry.get()
        new_text = f"{current_text}{name}"
        self.operation_entry.delete(0, tk.END)
        self.operation_entry.insert(0, new_text)

    def num_pad_click(self, value):
        current_text = self.operation_entry.get()
        new_text = f"{current_text}{value}"
        self.operation_entry.delete(0, tk.END)
        self.operation_entry.insert(0, new_text)

    def perform_operation(self, operation):
        current_text = self.operation_entry.get()
        if operation == 'DEL':
            self.operation_entry.delete(len(current_text) - 1)
        elif operation == 'AC':
            self.operation_entry.delete(0, tk.END)
        else:
            try:
                if operation == 'inv':
                    matrix_name = current_text.strip()
                    result = np.linalg.inv(self.matrices[matrix_name])
                elif operation in ['+', '-', '*']:
                    operands = current_text.split(operation)
                    matrix1 = self.matrices[operands[0].strip()]
                    matrix2 = self.matrices[operands[1].strip()]
                    if operation == '+':
                        result = matrix1 + matrix2
                    elif operation == '-':
                        result = matrix1 - matrix2
                    elif operation == '*':
                        result = np.dot(matrix1, matrix2)
                elif operation == '=':
                    result = eval(current_text, {"__builtins__": None}, self.matrices)

                self.result_label.config(text=f"Result:\n{result}")
            except Exception as e:
                self.result_label.config(text=f"Error:\n{e}")

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
