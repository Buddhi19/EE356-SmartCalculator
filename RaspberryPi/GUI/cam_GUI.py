import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from picamera2 import Picamera2
import threading
import time
import RPi.GPIO as GPIO
import os
import sys

parent_dir = os.path.dirname(os.path.abspath(__file__))

class CameraApp(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        self.camera = Picamera2()
        self.camera.configure(self.camera.create_preview_configuration(main={"size": (640, 480)}))
        self.camera.start()
        
        self.label = tk.Label(self)
        self.label.pack()
        
        self.capture_button = tk.Button(self, text="Capture", command=self.capture_image)
        self.capture_button.pack()
        
        self.back_button = tk.Button(self, text="Back", command=self.back)
        self.back_button.pack()

        self.stop_event = threading.Event()
        self.preview_thread = threading.Thread(target=self.update_preview)
        self.preview_thread.daemon = True
        self.preview_thread.start()
        
        # Setup GPIO
        self.flash_pin = 12
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.flash_pin, GPIO.OUT)
        GPIO.output(self.flash_pin, GPIO.LOW)

    def back(self):
        self.stop_camera()
        self.controller.show_frame("StartPage")
    
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
            
            # Capture high-resolution image
            frame = self.camera.capture_array()
            image = Image.fromarray(frame)
            
            # Flip the image vertically and horizontally
            image = image.transpose(Image.FLIP_TOP_BOTTOM).transpose(Image.FLIP_LEFT_RIGHT)
            
            image.save(parent_dir+"/camera/captured_image.png")
            
            # Restore preview configuration
            self.camera.stop()
            messagebox.showinfo("Image Capture", "Image Saved")
            self.controller.show_frame("Camera_Result_Page")

        except Exception as e:
            messagebox.showerror("Capture Error", str(e))
        finally:
            GPIO.output(self.flash_pin, GPIO.LOW)  # Ensure the flash is turned off
    
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

    def on_show(self):
        self.start_camera()
    
    def on_hide(self):
        self.stop_camera()

    def __del__(self):
        self.stop_camera()
        GPIO.cleanup()
        GPIO.cleanup()
    