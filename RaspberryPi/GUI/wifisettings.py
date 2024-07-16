import tkinter as tk
from tkinter import ttk
import subprocess
import re

class WiFiSettingsFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        # Wi-Fi network list
        self.network_listbox = tk.Listbox(self, width=40, height=10)
        self.network_listbox.pack(pady=10)

        # Scan button
        scan_button = ttk.Button(self, text="Scan for Networks", command=self.scan_networks)
        scan_button.pack(pady=5)

        # SSID and password entry fields
        self.ssid_var = tk.StringVar()
        self.pw_var = tk.StringVar()

        ssid_label = ttk.Label(self, text="SSID:")
        ssid_label.pack()
        self.ssid_entry = ttk.Entry(self, textvariable=self.ssid_var)
        self.ssid_entry.pack()

        pw_label = ttk.Label(self, text="Password:")
        pw_label.pack()
        self.pw_entry = ttk.Entry(self, textvariable=self.pw_var, show="*")
        self.pw_entry.pack()

        # Connect button
        connect_button = ttk.Button(self, text="Connect", command=self.connect_wifi)
        connect_button.pack(pady=10)

        # On-screen keyboard
        self.create_keyboard()

    def create_keyboard(self):
        keyboard_frame = ttk.Frame(self)
        keyboard_frame.pack(pady=10)

        keys = [
            '1234567890',
            'qwertyuiop',
            'asdfghjkl',
            'zxcvbnm',
            '!@#$%^&*()_+'
        ]

        for row, key_row in enumerate(keys):
            for col, key in enumerate(key_row):
                button = ttk.Button(keyboard_frame, text=key, width=3,
                                    command=lambda x=key: self.key_press(x))
                button.grid(row=row, column=col, padx=2, pady=2)

        # Space and backspace
        ttk.Button(keyboard_frame, text='Space', width=10,
                   command=lambda: self.key_press(' ')).grid(row=5, column=0, columnspan=5, pady=2)
        ttk.Button(keyboard_frame, text='←', width=10,
                   command=self.backspace).grid(row=5, column=5, columnspan=5, pady=2)

    def key_press(self, key):
        if self.focus_get() == self.ssid_entry:
            self.ssid_var.set(self.ssid_var.get() + key)
        elif self.focus_get() == self.pw_entry:
            self.pw_var.set(self.pw_var.get() + key)

    def backspace(self):
        if self.focus_get() == self.ssid_entry:
            self.ssid_var.set(self.ssid_var.get()[:-1])
        elif self.focus_get() == self.pw_entry:
            self.pw_var.set(self.pw_var.get()[:-1])

    def scan_networks(self):
        self.network_listbox.delete(0, tk.END)
        scan_result = subprocess.check_output(["sudo", "iwlist", "wlan0", "scan"]).decode('utf-8')
        networks = re.findall(r'ESSID:"(.*?)"', scan_result)
        for network in networks:
            self.network_listbox.insert(tk.END, network)

    def connect_wifi(self):
        ssid = self.ssid_var.get()
        password = self.pw_var.get()
        
        # Here you would implement the actual Wi-Fi connection logic
        # This is a placeholder for demonstration purposes
        print(f"Connecting to {ssid} with password {password}")