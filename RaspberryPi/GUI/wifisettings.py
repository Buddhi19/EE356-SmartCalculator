import tkinter as tk
from tkinter import ttk
import subprocess
import re

class WiFiSettingsFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#293C4A")
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        # Style configuration
        self.style = ttk.Style()
        self.style.theme_use('default')
        self.style.configure('TButton', background="#4A6572", foreground="white", font=('Arial', 12))
        self.style.map('TButton', background=[('active', "#5A7682")])
        self.style.configure('TLabel', background="#293C4A", foreground="white", font=('Arial', 12))
        self.style.configure('TEntry', fieldbackground="#293C4A", foreground="white", insertcolor="white", font=('Arial', 12))

        # Title
        title_label = ttk.Label(self, text="Wi-Fi Connection", style='TLabel', font=('Arial', 18, 'bold'))
        title_label.pack(pady=20)

        # Wi-Fi network list (initially hidden)
        self.list_frame = tk.Frame(self, bg="#293C4A")
        self.list_frame.pack(pady=10, expand=True, fill=tk.BOTH)
        self.list_frame.pack_forget()  # Initially hidden
        
        self.network_listbox = tk.Listbox(self.list_frame, width=40, height=10, bg="#293C4A", fg="white", font=('Arial', 12), selectbackground="#4A6572", selectforeground="white")
        self.network_listbox.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        scrollbar = ttk.Scrollbar(self.list_frame, orient=tk.VERTICAL, command=self.network_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.network_listbox.config(yscrollcommand=scrollbar.set)

        # Scan button
        scan_button = ttk.Button(self, text="Scan for Networks", command=self.scan_networks, style='TButton')
        scan_button.pack(pady=10)

        # SSID and password entry fields
        self.ssid_var = tk.StringVar()
        self.pw_var = tk.StringVar()

        ssid_label = ttk.Label(self, text="SSID:", style='TLabel')
        ssid_label.pack()
        self.ssid_entry = ttk.Entry(self, textvariable=self.ssid_var, style='TEntry',font=('Arial', 18))
        self.ssid_entry.pack(pady=5)

        pw_label = ttk.Label(self, text="Password:", style='TLabel')
        pw_label.pack()
        self.pw_entry = ttk.Entry(self, textvariable=self.pw_var, show="*", style='TEntry', font=('Arial', 18))
        self.pw_entry.pack(pady=5)

        # Connect button
        connect_button = ttk.Button(self, text="Connect", command=self.connect_wifi, style='TButton')
        connect_button.pack(pady=10)

        # On-screen keyboard
        self.create_keyboard()

    def create_keyboard(self):
        keyboard_frame = tk.Frame(self, bg="#293C4A")
        keyboard_frame.pack(pady=10, expand=True)

        self.is_shift_active = False

        keys = [
            '1234567890',
            'qwertyuiop',
            'asdfghjkl',
            'zxcvbnm'
        ]

        shift_keys = [
            '!@#$%^&*()',
            'QWERTYUIOP',
            'ASDFGHJKL',
            'ZXCVBNM'
        ]

        self.key_buttons = []

        for row, key_row in enumerate(keys):
            key_frame = tk.Frame(keyboard_frame, bg="#293C4A")
            key_frame.pack()
            for col, key in enumerate(key_row):
                button = tk.Button(key_frame, text=key, width=2, height=2,
                                command=lambda x=key, r=row, c=col: self.key_press(x, r, c),
                                bg="#4A6572", fg="white", activebackground="#5A7682",
                                font=('Arial', 11, 'bold'))
                button.pack(side=tk.LEFT, padx=2, pady=2)
                self.key_buttons.append((button, key, shift_keys[row][col]))

        # Space, backspace, and shift
        bottom_frame = tk.Frame(keyboard_frame, bg="#293C4A")
        bottom_frame.pack()
        
        self.shift_button = tk.Button(bottom_frame, text='Shift', width=10, height=2,
                                    command=self.toggle_shift,
                                    bg="#4A6572", fg="white", activebackground="#5A7682",
                                    font=('Arial', 10, 'bold'))
        self.shift_button.pack(side=tk.LEFT, padx=2, pady=2)
        
        tk.Button(bottom_frame, text='Space', width=10, height=2,
                command=lambda: self.key_press(' '),
                bg="#4A6572", fg="white", activebackground="#5A7682",
                font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=2, pady=2)
        
        tk.Button(bottom_frame, text='←', width=10, height=2,
                command=self.backspace,
                bg="#4A6572", fg="white", activebackground="#5A7682",
                font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=2, pady=2)

        back_button = ttk.Button(self, text="Back", command=lambda: self.controller.show_frame("StartPage2"), style='TButton')
        back_button.pack(pady=10)

    def toggle_shift(self):
        self.is_shift_active = not self.is_shift_active
        for button, lower, upper in self.key_buttons:
            button.config(text=upper if self.is_shift_active else lower)
        self.shift_button.config(relief=tk.SUNKEN if self.is_shift_active else tk.RAISED)

    def key_press(self, key, row=None, col=None):
        if row is not None and col is not None and self.is_shift_active:
            key = self.key_buttons[row * 10 + col][2]  # Get the shift version of the key
        
        if self.focus_get() == self.ssid_entry:
            self.ssid_var.set(self.ssid_var.get() + key)
        elif self.focus_get() == self.pw_entry:
            self.pw_var.set(self.pw_var.get() + key)
        
        if self.is_shift_active:
            self.toggle_shift()  # Turn off shift after one capital letter

    def backspace(self):
        if self.focus_get() == self.ssid_entry:
            self.ssid_var.set(self.ssid_var.get()[:-1])
        elif self.focus_get() == self.pw_entry:
            self.pw_var.set(self.pw_var.get()[:-1])

    def scan_networks(self):
        self.network_listbox.delete(0, tk.END)
        try:
            scan_result = subprocess.check_output(["sudo", "iwlist", "wlan0", "scan"]).decode('utf-8')
            networks = re.findall(r'ESSID:"(.*?)"', scan_result)
            if networks:
                for network in networks:
                    self.network_listbox.insert(tk.END, network)
                self.list_frame.pack(pady=10, expand=True, fill=tk.BOTH)  # Show the list frame
            else:
                self.show_message("No networks found.")
        except subprocess.CalledProcessError:
            self.show_message("Error scanning networks. Please try again.")

    def show_message(self, message):
        # Remove the list frame if it's visible
        self.list_frame.pack_forget()
        
        # Show a message to the user
        msg_label = ttk.Label(self, text=message, style='TLabel', font=('Arial', 12))
        msg_label.pack(pady=10)
        self.after(3000, msg_label.destroy)  # Remove the message after 3 seconds

    def connect_wifi(self):
        ssid = self.ssid_var.get()
        password = self.pw_var.get()
        
        # Here you would implement the actual Wi-Fi connection logic
        # This is a placeholder for demonstration purposes
        print(f"Connecting to {ssid} with password {password}")