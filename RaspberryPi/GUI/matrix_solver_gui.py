import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
from tkinter import ttk
import numpy as np
from matrix_solver import MatrixSolver
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
            print(row)
        self.callback(self.matrix_name, matrix)
        self.destroy()

class MatrixOperationPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="#293C4A")

        self.matrices = {name: None for name in ['MatA', 'MatB', 'MatC', 'MatD', 'MatE']}
        self.solver = MatrixSolver(self.matrices['MatA'], self.matrices['MatB'], self.matrices['MatC'], self.matrices['MatD'], self.matrices['MatE'])

        self.label = tk.Label(self, text="Matrix Operations", font=('sans-serif', 20, 'bold'), bg="#293C4A", fg="#BBB")
        self.label.pack(pady=20)

        self.operation_entry = tk.Entry(self, font=('sans-serif', 15, 'bold'), bg="#BBB", fg="#000", justify='right', width=25)
        self.operation_entry.pack(pady=10)

        self.result_label = tk.Label(self, text="", font=('sans-serif', 15, 'bold'), bg="#293C4A", fg="#BBB")
        self.result_label.pack(pady=10)

        self.operation_pad_frame = tk.Frame(self, bg="#293C4A")
        self.operation_pad_frame.pack(pady=10)

        arrow_keys = {'←':"left", '→':"right"}
        arrows = ['←','→']
        operations = ['+', '-', '*', 'inv' ]
        special_operations = ['=', 'DEL', 'AC']
        matrices_row = ['MatA', 'MatB', 'MatC', 'MatD', 'MatE']
        self.operation_buttons = []
        self.matrix_buttons = []

        for arrow in arrow_keys:
            button = tk.Button(self.operation_pad_frame, text=arrow, command=lambda a=arrow: self.perform_operation(arrow_keys[a]),
                               font=('sans-serif', 12, 'bold'), bg="#BBB", fg="#000", width=4)
            button.grid(row=0, column= 1+ arrows.index(arrow), padx=3, pady=5)
            self.operation_buttons.append(button)

        for matrix in matrices_row:
            button = tk.Button(self.operation_pad_frame, text=matrix, command=lambda o=matrix: self.perform_operation(o),
                               font=('sans-serif', 12, 'bold'), bg="#BBB", fg="#000", width=4)
            button.grid(row=3, column=matrices_row.index(matrix), padx=3, pady=5)
            self.matrix_buttons.append(button)

        for op in operations:
            button = tk.Button(self.operation_pad_frame, text=op, command=lambda o=op: self.perform_operation(o),
                               font=('sans-serif', 12, 'bold'), bg="#BBB", fg="#000", width=4)
            button.grid(row=1, column=operations.index(op), padx=3, pady=5)
            self.operation_buttons.append(button)

        for sop in special_operations:
            button = tk.Button(self.operation_pad_frame, text=sop, command=lambda o=sop: self.perform_operation(o),
                               font=('sans-serif', 12, 'bold'), bg="#BBB", fg="#000", width=4)
            button.grid(row=2, column=1+special_operations.index(sop), padx=3, pady=5)
            self.operation_buttons.append(button)    

        self.matrix_buttons_frame = tk.Frame(self, bg="#293C4A")
        self.matrix_buttons_frame.pack(pady=10)

        self.num_pad_frame = tk.Frame(self, bg="#293C4A")
        self.num_pad_frame.pack(pady=10)

        self.num_pad = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2),
            ('0', 4, 1), ('.', 4, 0), ('-', 4, 2)
        ]

        for (text, row, col) in self.num_pad:
            button = tk.Button(self.num_pad_frame, text=text, command=lambda t=text: self.perform_operation(t),
                               font=('sans-serif', 15, 'bold'), bg="#BBB", fg="#000", width=5)
            button.grid(row=row, column=col)

        add_matrix_button = tk.Button(self, text="Add Matrix", command=self.add_matrix,
                                      font=('sans-serif', 15, 'bold'), bg="#BBB", fg="#000")
        add_matrix_button.pack(pady=20)

        back_button = tk.Button(self, text="Back", command=lambda: controller.show_frame("StartPage"),
                                font=('sans-serif', 15, 'bold'), bg="#BBB", fg="#000")
        back_button.pack(pady=10)
        


    def update_matrix_buttons(self):
        for widget in self.matrix_buttons_frame.winfo_children():
            widget.destroy()

        for name in self.matrices.keys():
            button = tk.Button(self.matrix_buttons_frame, text=name, command=lambda n=name: self.perform_operation(n),
                               font=('sans-serif', 15, 'bold'), bg="#BBB", fg="#000", width=5)
            button.pack(side=tk.LEFT, padx=5)

    def add_matrix(self):
        self.matrix_input_page = MatrixInputPage(self, self.open_matrix_entry_page)

    def open_matrix_entry_page(self, rows, cols, matrix_name):
        self.matrix_entry_page = MatrixEntryPage(self, self.store_matrix)
        self.matrix_entry_page.set_matrix_details(rows, cols, matrix_name)

    def store_matrix(self, name, matrix):
        self.matrices[name] = matrix
        self.solver.update_matrix(self.matrices['MatA'], self.matrices['MatB'], self.matrices['MatC'], self.matrices['MatD'], self.matrices['MatE'])

    def set_matrix(self, name):
        current_text = self.operation_entry.get()
        new_text = f"{current_text}{name}"
        self.operation_entry.delete(0, tk.END)
        self.operation_entry.insert(0, new_text) 

    def perform_operation(self, operation):
        self.solver.user_input(operation)
        self.operation_entry.delete(0, tk.END)
        self.operation_entry.insert(0, self.solver.showing_exp)
        if operation == "=":
            self.result_label.config(text=self.solver.result)
        print(self.solver.result)

        

if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg="#293C4A")
    root.geometry("330x800")
    root.title("Standalone Calculator")

    # Initialize the Calculator frame
    calculator_frame = MatrixOperationPage(root, root)
    calculator_frame.pack(fill="both", expand=True)
    root.mainloop()