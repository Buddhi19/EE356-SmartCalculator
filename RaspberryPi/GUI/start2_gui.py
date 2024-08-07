import tkinter as tk
from tkinter import ttk
import os
import sys
from PIL import Image, ImageTk

parent_dir = os.path.dirname(os.path.abspath(__file__))

class StartPage2(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="#293C4A")
        self.wifi_label = None  # Initialize wifi_label
        self.create_widgets2()

    def create_widgets2(self):
        label = tk.Label(self, text="Solvista", bg="#293C4A", fg="white", font=("Arial", 30, "bold"))
        label.grid(row=0, column=0, columnspan=2, pady=10)

        self.wifi_logo()

        buttons = [
            ("Fourier Transform", "FourierTransform", parent_dir + "\\icons\\integrals.png"),
            ("Laplace Transform", "LaplaceTransform", parent_dir + "\\icons\\laplace.png"),
            ("Z Transform", "DiscreteSignalCalculator", parent_dir + "\\icons\\z_transform.png"),
            ("Normal Distribution", "NormalDistributionCalculator", parent_dir + "\\icons\\prob.png"),
            ("Settings", "WiFiSettingsFrame", parent_dir + "\\icons\\settings.png")
        ]
        if sys.platform == "linux":
            buttons = [
                ("Fourier Transform", "FourierTransform", parent_dir + "/icons/integrals.png"),
                ("Laplace Transform", "LaplaceTransform", parent_dir + "/icons/laplace.png"),
                ("Z Transform", "DiscreteSignalCalculator", parent_dir + "/icons/z_transform.png"),
                ("Normal Distribution", "NormalDistributionCalculator", parent_dir + "/icons/prob.png"),
                ("Settings", "WiFiSettingsFrame", parent_dir + "/icons/settings.png")
            ]

        for i, (text, frame_name, image_path) in enumerate(buttons):
            try:
                image = Image.open(image_path)
                image = image.resize((80, 80), Image.LANCZOS)
                photo = ImageTk.PhotoImage(image)

                button = tk.Button(self, text=text, image=photo, compound="top", command=lambda name=frame_name: self.controller.show_frame(name),
                                   font=("Arial", 13, "bold"), width=200, bg="#293C4A", borderwidth=0, highlightthickness=0,
                                   fg="white",pady=10)
                button.image = photo  # keep a reference to the image
                button.grid(row=(i//2) + 1, column=i % 2, pady=15, padx=10, sticky="nsew")
            except Exception as e:
                print(f"Error loading image for {text}: {e}")
                button = tk.Button(self, text=text, compound="left", command=lambda name=frame_name: self.controller.show_frame(name),
                                   font=("sans-serif", 15, "bold"), width=200, bg="white", borderwidth=2, highlightthickness=0, highlightbackground="#000000")
                button.grid(row=(i//2) + 1, column=i % 2, pady=15, padx=20, sticky="nsew")

        go_back_button = tk.Button(self, text="1", command=lambda: self.controller.show_frame("StartPage"), font=("sans-serif", 15, "bold"), borderwidth=0, 
                                            highlightthickness=0, bg="#293C4A", fg="white", 
                                            activebackground="#293C4A", activeforeground="white")
        go_back_button.grid(row=6, column=0, padx=1, sticky='e')

        current_page_num_button = tk.Button(self, text="2", command=self.current_button,
                                            font=("sans-serif", 20, "bold"), width=2, borderwidth=0,
                                            highlightthickness=0, bg="#293C4A", fg="white",
                                            activebackground="#293C4A", activeforeground="white")
        current_page_num_button.grid(row=6, column=1, padx=1, sticky='w')


        # Make the grid cells expand proportionally
        for row in range((len(buttons)//2) + 3):
            if row == 6 or row == 7:
                self.grid_rowconfigure(row)
                continue
            self.grid_rowconfigure(row, weight=1)
        for col in range(2):
            self.grid_columnconfigure(col, weight=1)

    def current_button(self):
        pass

    def wifi_logo(self):
        if self.controller.is_connected():
            self.add_wifi_logo("wifi_on")
        else:
            self.add_wifi_logo("wifi_off")
        self.after(2000, self.wifi_logo)

    def add_wifi_logo(self, state):
        wifi_image_path = parent_dir + f"\\icons\\{state}.png" if sys.platform == "win32" else parent_dir + f"/icons/{state}.png"
        try:
            wifi_image = Image.open(wifi_image_path)
            wifi_image = wifi_image.resize((30, 30), Image.LANCZOS)
            wifi_photo = ImageTk.PhotoImage(wifi_image)

            if self.wifi_label is None:
                self.wifi_label = tk.Label(self, image=wifi_photo, bg="#293C4A")
                self.wifi_label.grid(row=0, column=1, sticky="ne", padx=10, pady=10)
            else:
                self.wifi_label.configure(image=wifi_photo)
            self.wifi_label.image = wifi_photo  # keep a reference to the image
        except Exception as e:
            print(f"Error loading Wi-Fi logo: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Standalone Calculator")
    root.configure(bg="#293C4A", bd=10)
    root.geometry("400x800")
    StartPage2(root, None).pack()
    root.mainloop()
