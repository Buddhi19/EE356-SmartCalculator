import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from picamera2 import Picamera2
import threading
import time
import RPi.GPIO as GPIO
import os
import io
import requests  # Add this import

parent_dir = os.path.dirname(os.path.abspath(__file__))

class CameraApp(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#293C4A")
        self.controller = controller
        self.display_var = tk.StringVar()
        
        self.camera = Picamera2()
        self.camera.configure(self.camera.create_preview_configuration(main={"size": (640, 480)}))
        self.camera.start()
        
        button_params_main = {'fg': '#000', 'bg': '#BBB', 'font': ('sans-serif', 15, 'bold'), 'height': 1}
        
        self.label = tk.Label(self)
        self.label.grid(row=1, column=0, columnspan=4, sticky="nsew")
        
        self.capture_button = tk.Button(self, text="Capture", command=self.capture_image,**button_params_main,width=10)
        self.capture_button.grid(row=2, column=0, sticky="nsew")
        
        self.back_button = tk.Button(self, text="Back", command=self.back,**button_params_main,width=10)
        self.back_button.grid(row=2, column=1, sticky="nsew")
        
        self.create_widgets()

        self.stop_event = threading.Event()
        self.preview_thread = threading.Thread(target=self.update_preview)
        self.preview_thread.daemon = True
        self.preview_thread.start()
        
        # Setup GPIO
        self.flash_pin = 12
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.flash_pin, GPIO.OUT)
        GPIO.output(self.flash_pin, GPIO.LOW)
        
    def create_widgets(self):
        self.entry = tk.Entry(self, textvariable=self.display_var, font=('sans-serif', 20, 'bold'), justify='right', state='readonly')
        self.entry.grid(row=0, column=0, columnspan=4, ipady=30, sticky="nsew")
        
        button_params_main = {'fg': '#000', 'bg': '#BBB', 'font': ('sans-serif', 15, 'bold'), 'height': 1}
        
        self.mode_button = tk.Button(self, text="Mode", command=lambda: ModeSelection_Whiteboard(self, self.set_mode), **button_params_main)
        self.mode_button.grid(row=3, column=0, sticky="nsew")
        
        self.DEL_button = tk.Button(self, text="DEL", command=self.delete, **button_params_main)
        self.DEL_button.grid(row=3, column=1, sticky="nsew")

        self.AC_button = tk.Button(self, text="AC", command=self.clear, **button_params_main)
        self.AC_button.grid(row=4, column=0, sticky="nsew")
        
    def delete(self):
        self.display_var.set(self.display_var.get()[:-1])

    def clear(self):
        self.display_var.set("")

    def set_mode(self, mode):
        self.mode = mode
        print(f"Mode set to: {mode}")
        self.update_solve_button()

    def back(self):
        self.stop_camera()
        self.controller.show_frame("StartPage")
    
    def on_show(self):
        self.start_camera()
        
    def on_hide(self):
        self.stop_camera()
    
    def update_preview(self):
        while not self.stop_event.is_set():
            frame = self.camera.capture_array()
            image = Image.fromarray(frame)
            image = image.transpose(Image.FLIP_TOP_BOTTOM).transpose(Image.FLIP_LEFT_RIGHT)
            image = ImageTk.PhotoImage(image)
            self.label.config(image=image)
            self.label.image = image
            time.sleep(0.1)  # Adjust this value to control frame rate
    
    def capture_image(self):
        try:
            if not self.camera:
                messagebox.showwarning("Camera Error", "Camera is not active")
                return
            
            # Flash ON
            GPIO.output(self.flash_pin, GPIO.HIGH)
            time.sleep(0.1)  # Short delay to ensure flash is on before capture
            
            # Capture high-resolution image
            self.camera.stop()
            self.camera.configure(self.camera.create_still_configuration(main={"size": (1920, 1080)}))
            self.camera.start()
            frame = self.camera.capture_array()
            image = Image.fromarray(frame)
            
            # Flip the image vertically and horizontally
            image = image.transpose(Image.FLIP_TOP_BOTTOM).transpose(Image.FLIP_LEFT_RIGHT)
            
            image_path = os.path.join(parent_dir, "captured_image.png")
            image.save(image_path)
            
            # Restore preview configuration
            self.camera.stop()
            self.camera.configure(self.camera.create_preview_configuration(main={"size": (640, 480)}))
            self.camera.start()
            
            # Flash OFF
            GPIO.output(self.flash_pin, GPIO.LOW)
            
            # Post the image to the server
            with open(image_path, 'rb') as img_file:
                response = requests.post('http://your-server-url/upload', files={'file': img_file})
                response_data = response.json()
                
            if response.status_code == 200 and 'equations' in response_data:
                self.show_equations(response_data['equations'])
            else:
                messagebox.showerror("Error", "Failed to process the image. Please try again.")
            
        except Exception as e:
            messagebox.showerror("Capture Error", str(e))
        finally:
            GPIO.output(self.flash_pin, GPIO.LOW)  # Ensure the flash is turned off
    
    def show_equations(self, equations):
        def add_equations():
            self.display_var.set(" + ".join(equations))
            eq_window.destroy()

        def retry_capture():
            eq_window.destroy()
            self.capture_image()

        eq_window = tk.Toplevel(self)
        eq_window.title("Equations Found")
        eq_window.geometry("400x300")
        
        msg = tk.Message(eq_window, text="\n".join(equations), width=380)
        msg.pack(pady=10)
        
        add_button = tk.Button(eq_window, text="Add", command=add_equations)
        add_button.pack(side=tk.LEFT, padx=10, pady=10)
        
        retry_button = tk.Button(eq_window, text="Retry", command=retry_capture)
        retry_button.pack(side=tk.RIGHT, padx=10, pady=10)

    def pack(self, **kwargs):
        super().pack(**kwargs)
        self.start_camera()
    
    def pack_forget(self):
        self.stop_camera()
        super().pack_forget()
    
    def grid(self, **kwargs):
        super().grid(**kwargs)
        self.start_camera()
    
    def grid_forget(self):
        self.stop_camera()
        super().grid_forget()
    
    def place(self, **kwargs):
        super().place(**kwargs)
        self.start_camera()
    
    def place_forget(self):
        self.stop_camera()
        super().place_forget()
        
    def start_camera(self):
        if not self.camera:
            self.camera = Picamera2()
            self.camera.configure(self.camera.create_preview_configuration(main={"size": (640, 480)}))
            self.camera.start()
            self.update_preview()
    
    def stop_camera(self):
        if self.camera:
            self.stop_event.set()
            self.camera.stop()
            self.camera.close()
            self.camera = None

    def __del__(self):
        self.stop_camera()
        GPIO.cleanup()
        
class ModeSelection_Whiteboard(tk.Toplevel):
    def __init__(self, parent, callback):
        super().__init__(parent, bg="#293C4A")
        self.callback = callback
        self.mode_list = [
            "Calculate", "Plot", "Transfer Function", "Simultaneous Equations", "Matrix"
        ]
        self.create_widgets()

    def create_widgets(self):
        button_params_main = {'fg': '#000', 'bg': '#BBB', 'font': ('sans-serif', 10, 'bold')}
        for mode in self.mode_list:
            button = tk.Button(self, text=mode, command=lambda m=mode: self.select_mode(m),**button_params_main)
            button.pack(fill=tk.X, pady=5)

    def select_mode(self, mode):
        self.callback(mode)
        self.destroy()

# Make sure to replace 'http://your-server-url/upload' with your actual server URL
