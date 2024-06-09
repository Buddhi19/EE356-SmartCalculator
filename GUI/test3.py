import tkinter as tk
from tkinter import ttk

class MainMenu(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Smart Calculator Main Menu")
        self.geometry("400x300")
        self.configure(bg="#293C4A")

        # Welcome Label
        self.label = ttk.Label(self, text="Welcome", font=("Helvetica", 20, 'bold'), background="#293C4A", foreground="#BBB")
        self.label.pack(pady=10)

        # Frame to hold buttons
        self.button_frame = tk.Frame(self, bg="#293C4A")
        self.button_frame.pack(fill=tk.BOTH, expand=True)

        # Create a custom style for buttons
        self.style = ttk.Style()
        self.style.configure('Custom.TButton', font=('Helvetica', 12))

        # Adding buttons to the frame
        self.scientific_button = ttk.Button(self.button_frame, text="Scientific Calculator", command=self.open_scientific_calculator, style='Custom.TButton', width=20)
        self.scientific_button.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.graphing_button = ttk.Button(self.button_frame, text="Graphing Calculator", command=self.open_graphing_calculator, style='Custom.TButton', width=20)
        self.graphing_button.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.camera_button = ttk.Button(self.button_frame, text="Camera", command=self.open_camera, style='Custom.TButton', width=20)
        self.camera_button.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.ebook_button = ttk.Button(self.button_frame, text="Ebook", command=self.open_ebook, style='Custom.TButton', width=20)
        self.ebook_button.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        # Configure grid weights to make buttons expandable
        self.button_frame.columnconfigure(0, weight=1)
        self.button_frame.columnconfigure(1, weight=1)
        self.button_frame.rowconfigure(0, weight=1)
        self.button_frame.rowconfigure(1, weight=1)

    def open_scientific_calculator(self):
        # Code to open the Scientific Calculator GUI
        pass

    def open_graphing_calculator(self):
        # Code to open the Graphing Calculator GUI
        pass

    def open_camera(self):
        # Code to open the Camera GUI
        pass

    def open_ebook(self):
        # Code to open the Ebook GUI
        pass

if __name__ == "__main__":
    app = MainMenu()
    app.mainloop()
