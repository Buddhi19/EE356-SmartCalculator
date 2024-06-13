import tkinter as tk
from tkinter import ttk

class Loading_GUI(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        self.configure(bg="#293C4A")
        self.loading_label = ttk.Label(self, text="Loading...", font=('sans-serif', 20, 'bold'), background="#293C4A", foreground="#FFF")
        self.loading_label.pack(pady=10)

        self.progress = ttk.Progressbar(self, orient="horizontal", length=300, mode="indeterminate")
        self.progress.pack(pady=10)

        self.back_button = ttk.Button(self, text="Back", command=lambda: self.controller.show_frame("StartPage"))
        self.back_button.pack(pady=10)
        