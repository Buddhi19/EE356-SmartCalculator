import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

parent_dir = os.path.dirname(os.path.abspath(__file__))

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from picamera import PiCamera
from io import BytesIO
import RPi.GPIO as GPIO
import time
from cam_solver_server import post_image

class CameraApp(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        self.camera = None  # Camera will be initialized when the frame is shown
        self.flash_pin = 12

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.flash_pin, GPIO.OUT)
        GPIO.output(self.flash_pin, GPIO.LOW)

        self.configure(width=480, height=600)
        self.pack_propagate(False)
        self.create_widgets()

    def create_widgets(self):
        self.capture_button = tk.Button(self, text="Capture", command=self.capture_image)
        self.capture_button.pack(side="bottom")

        self.image_label = tk.Label(self)
        self.image_label.pack(side="top")

        back_button = tk.Button(self, text="Back", command=self.back)
        back_button.pack(side="bottom")
        
    def back(self):
        self.stop_camera()
        self.controller.show_frame("StartPage")

    def start_camera(self):
        if not self.camera:
            self.camera = PiCamera()
            self.camera.resolution = (640, 480)  # Lower resolution for preview
            self.update_image()

    def stop_camera(self):
        if self.camera:
            self.camera.close()
            self.camera = None

    def update_image(self):
        if not self.camera:
            return
        stream = BytesIO()
        self.camera.capture(stream, format='jpeg', use_video_port=True)
        stream.seek(0)
        image = Image.open(stream)
        image = image.transpose(Image.FLIP_TOP_BOTTOM).transpose(Image.FLIP_LEFT_RIGHT)  # Flip the image vertically and horizontally
        self.photo = ImageTk.PhotoImage(image)
        self.image_label.configure(image=self.photo)
        self.after(50, self.update_image)  # Refresh the image every 50 ms

    def capture_image(self):
        if not self.camera:
            messagebox.showwarning("Camera Error", "Camera is not active")
            return
        
        # Flash ON
        GPIO.output(self.flash_pin, GPIO.HIGH)
        time.sleep(0.1)  # Short delay to ensure flash is on before capture
        
        stream = BytesIO()
        self.camera.resolution = (1920, 1080)  # High resolution for capture
        self.camera.capture(stream, format='png')
        self.camera.resolution = (640, 480)  # Restore preview resolution
        stream.seek(0)
        self.captured_image = Image.open(stream)
        self.captured_image.save(parent_dir+"/captured_image.png")
        
        # Flash OFF
        GPIO.output(self.flash_pin, GPIO.LOW)
        self.stop_camera()

        self.show_captured_image(self.captured_image)
        
    def show_captured_image(self, image):
        self.photo = ImageTk.PhotoImage(image)
        self.image_label.configure(image=self.photo)
        self.capture_button.pack_forget()

        self.recapture_button = tk.Button(self, text="Recapture", command=self.recapture_image)
        self.recapture_button.pack(side="left")
        
        self.process_button = tk.Button(self, text="Process", command=self.process_image)
        self.process_button.pack(side="right")

    def recapture_image(self):
        self.recapture_button.pack_forget()
        self.process_button.pack_forget()
        self.capture_button.pack(side="bottom")
        self.start_camera()

    def process_image(self):
        ans = post_image(parent_dir+"/captured_image.png")
        messagebox.showinfo("Result", ans)


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

    def __del__(self):
        GPIO.cleanup()


        
    
        