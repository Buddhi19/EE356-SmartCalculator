import tkinter as tk
from tkinter import ttk
import subprocess
import re

class MobileKeyboard(tk.Frame):
    def __init__(self, parent, entry_widget, button_params):
        tk.Frame.__init__(self, parent, bg="#3C3636")
        self.entry = entry_widget
        self.button_params = button_params
        self.create_keyboard()

    def create_keyboard(self):
        keys = [
            ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
            ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
            ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l'],
            ['z', 'x', 'c', 'v', 'b', 'n', 'm'],
            ['@', '#', '_', '&', '-', '+', '(', ')', '/']
        ]
        for row, key_row in enumerate(keys):
            key_frame = tk.Frame(self, bg="#3C3636")
            key_frame.pack()
            for key in key_row:
                button = tk.Button(key_frame, text=key, width=3, height=2,
                                   command=lambda x=key: self.press(x),
                                   **self.button_params)
                button.pack(side=tk.LEFT)
        
        # Special keys
        bottom_frame = tk.Frame(self, bg="#3C3636")
        bottom_frame.pack(pady=2)
        tk.Button(bottom_frame, text='Space', width=20, command=lambda: self.press(' '),
                  **self.button_params).pack(side=tk.LEFT, padx=1)
        tk.Button(bottom_frame, text='⌫', width=5, command=self.backspace,
                  **self.button_params).pack(side=tk.LEFT, padx=1)

    def press(self, key):
        current = self.entry.get()
        self.entry.delete(0, tk.END)
        self.entry.insert(0, current + key)

    def backspace(self):
        current = self.entry.get()
        self.entry.delete(0, tk.END)
        self.entry.insert(0, current[:-1])

class WiFiSettingsFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg="#293C4A")
        self.parent = parent
        self.create_widgets()

    def create_widgets(self):
        # Title
        title_label = tk.Label(self, text="WiFi Settings", font=("sans-serif", 18, "bold"), bg="#293C4A", fg="#BBB")
        title_label.pack(pady=15)

        # Scan frame
        scan_frame = tk.Frame(self, bg="#3C3636", bd=2, relief=tk.GROOVE)
        scan_frame.pack(padx=10, pady=5, fill=tk.X)

        scan_label = tk.Label(scan_frame, text="Available Networks", font=("sans-serif", 12, "bold"), bg="#3C3636", fg="#BBB")
        scan_label.pack(pady=5)

        self.scan_button = tk.Button(scan_frame, text="Scan for WiFi", command=self.scan_wifi,
                                     **self.parent.button_params_other)
        self.scan_button.pack(pady=5)

        self.wifi_listbox = tk.Listbox(scan_frame, width=35, height=4, font=("sans-serif", 10), bg="#3C3636", fg="#BBB")
        self.wifi_listbox.pack(pady=5)

        back_button = tk.Button(self, text="Back", command=lambda: self.controller.show_frame("StartPage"), font=("sans-serif", 12, "bold"), bg="#3C3636", fg="#BBB")
        back_button.pack(pady=5)

        # Connect frame
        connect_frame = tk.Frame(self, bg="#3C3636", bd=2, relief=tk.GROOVE)
        connect_frame.pack(padx=10, pady=5, fill=tk.X)

        connect_label = tk.Label(connect_frame, text="Connect to Network", font=("sans-serif", 12, "bold"), bg="#3C3636", fg="#BBB")
        connect_label.pack(pady=5)

        tk.Label(connect_frame, text="SSID:", bg="#3C3636", fg="#BBB", font=("sans-serif", 10)).pack()
        self.ssid_entry = tk.Entry(connect_frame, width=30, font=("sans-serif", 10), bg="#555", fg="#BBB", insertbackground="#BBB")
        self.ssid_entry.pack(pady=2)
        self.ssid_entry.bind("<FocusIn>", lambda event: self.show_keyboard(self.ssid_entry))

        tk.Label(connect_frame, text="Password:", bg="#3C3636", fg="#BBB", font=("sans-serif", 10)).pack()
        self.password_entry = tk.Entry(connect_frame, show="*", width=30, font=("sans-serif", 10), bg="#555", fg="#BBB", insertbackground="#BBB")
        self.password_entry.pack(pady=2)
        self.password_entry.bind("<FocusIn>", lambda event: self.show_keyboard(self.password_entry))

        self.connect_button = tk.Button(connect_frame, text="Connect", command=self.connect_wifi,
                                        **self.parent.button_params_main)
        self.connect_button.pack(pady=5)

        self.status_label = tk.Label(connect_frame, text="", bg="#3C3636", fg="#BBB", font=("sans-serif", 10))
        self.status_label.pack(pady=5)

        self.keyboard_frame = tk.Frame(self, bg="#293C4A")
        self.keyboard_frame.pack(pady=5)

    def show_keyboard(self, entry_widget):
        # Clear any existing keyboard
        for widget in self.keyboard_frame.winfo_children():
            widget.destroy()
        # Create and show new keyboard
        self.keyboard = MobileKeyboard(self.keyboard_frame, entry_widget, self.parent.button_params)
        self.keyboard.pack()

    def scan_wifi(self):
        self.wifi_listbox.delete(0, tk.END)
        scan_result = subprocess.check_output(["sudo", "iwlist", "wlan0", "scan"]).decode("utf-8")
        ssids = re.findall(r'ESSID:"(.*?)"', scan_result)
        for ssid in ssids:
            self.wifi_listbox.insert(tk.END, ssid)

    def connect_wifi(self):
        ssid = self.ssid_entry.get()
        password = self.password_entry.get()

        wpa_supplicant_conf = f"""
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=US

network={{
    ssid="{ssid}"
    psk="{password}"
}}
"""
        with open("/etc/wpa_supplicant/wpa_supplicant.conf", "w") as f:
            f.write(wpa_supplicant_conf)

        subprocess.run(["sudo", "wpa_cli", "-i", "wlan0", "reconfigure"])
        self.status_label.config(text="Connecting...", fg="#FFA500")
        self.after(5000, self.check_connection)

    def check_connection(self):
        try:
            subprocess.check_output(["ping", "-c", "1", "8.8.8.8"])
            self.status_label.config(text="Connected successfully!", fg="#4CAF50")
        except subprocess.CalledProcessError:
            self.status_label.config(text="Connection failed. Please try again.", fg="#FF0000")

class SettingsApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("WiFi Settings")
        self.geometry("330x800")
        self.configure(bg="#293C4A")
        
        self.button_params = {'fg': '#BBB', 'bg': '#3C3636', 'font': ('sans-serif', 11, 'bold')}
        self.button_params_main = { 'fg': '#000', 'bg': '#BBB', 'font': ('sans-serif', 11, 'bold')}
        self.button_params_other = {'fg': '#000', 'bg': '#db701f', 'font': ('sans-serif', 11, 'bold')}

        wifi_frame = WiFiSettingsFrame(self)
        wifi_frame.pack(expand=True, fill=tk.BOTH)

if __name__ == "__main__":
    app = SettingsApp()
    app.mainloop()