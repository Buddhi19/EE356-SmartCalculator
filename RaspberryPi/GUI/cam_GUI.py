import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from picamera import PiCamera
from picamera.array import PiRGBArray
import threading
import io
import time
import RPi.GPIO as GPIO

class CameraApp(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        self.camera = PiCamera()
        self.camera.resolution = (640, 480)  # Lower resolution for preview
        self.stream = PiRGBArray(self.camera)
        
        self.label = tk.Label(self)
        self.label.pack()
        
        self.capture_button = tk.Button(self, text="Capture", command=self.capture_image)
        self.capture_button.pack()
        
        self.back_button = tk.Button(self, text="Back", command=lambda: controller.show_frame("StartPage"))
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
    
    def update_preview(self):
        for frame in self.camera.capture_continuous(self.stream, format="rgb", use_video_port=True):
            if self.stop_event.is_set():
                break
            image = Image.fromarray(frame.array)
            self.stream.truncate(0)
            self.stream.seek(0)
            image = ImageTk.PhotoImage(image)
            self.label.config(image=image)
            self.label.image = image
    
    def capture_image(self):
        try:
            if not self.camera:
                messagebox.showwarning("Camera Error", "Camera is not active")
                return
            
            # Flash ON
            GPIO.output(self.flash_pin, GPIO.HIGH)
            time.sleep(0.1)  # Short delay to ensure flash is on before capture
            
            stream = io.BytesIO()
            self.camera.resolution = (1920, 1080)  # High resolution for capture
            self.camera.capture(stream, format='jpeg')
            self.camera.resolution = (640, 480)  # Restore preview resolution
            stream.seek(0)
            image = Image.open(stream)
            image = image.transpose(Image.FLIP_TOP_BOTTOM).transpose(Image.FLIP_LEFT_RIGHT)  # Flip the image vertically and horizontally
            image.save("captured_image.jpg")
            
            # Flash OFF
            GPIO.output(self.flash_pin, GPIO.LOW)
            
            messagebox.showinfo("Image Capture", "Image has been captured and saved as 'captured_image.jpg'")
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
            self.camera = PiCamera()
            self.camera.resolution = (640, 480)  # Lower resolution for preview
            self.update_image()

    def stop_camera(self):
        if self.camera:
            self.camera.close()
            self.camera = None

    def __del__(self):
        GPIO.cleanup()
