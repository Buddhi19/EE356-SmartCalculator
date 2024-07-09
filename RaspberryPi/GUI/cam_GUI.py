import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from picamera2 import Picamera2, Preview
from threading import Thread, Event
import io
import time

class CameraApp(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        self.camera = Picamera2()
        self.camera.configure(self.camera.create_preview_configuration(main={"size": (640, 480)}))
        
        self.label = tk.Label(self)
        self.label.pack()
        
        self.capture_button = tk.Button(self, text="Capture", command=self.capture_image)
        self.capture_button.pack()
        
        self.back_button = tk.Button(self, text="Back", command=lambda: controller.show_frame("StartPage"))
        self.back_button.pack()
        
        self.stop_event = Event()
        self.preview_thread = Thread(target=self.update_preview)
        self.preview_thread.daemon = True
        self.preview_thread.start()
    
    def update_preview(self):
        self.camera.start_preview(Preview.DRM)
        while not self.stop_event.is_set():
            frame = self.camera.capture_array()
            image = Image.fromarray(frame)
            image = ImageTk.PhotoImage(image)
            self.label.config(image=image)
            self.label.image = image
            time.sleep(0.1)  # Adjust the preview update rate if necessary
        
    def capture_image(self):
        try:
            if not self.camera:
                messagebox.showwarning("Camera Error", "Camera is not active")
                return
            
            
            self.camera.configure(self.camera.create_still_configuration(main={"size": (1920, 1080)}))
            self.camera.start()
            frame = self.camera.capture_array()
            image = Image.fromarray(frame)
            image = image.transpose(Image.FLIP_TOP_BOTTOM).transpose(Image.FLIP_LEFT_RIGHT)  # Flip the image vertically and horizontally
            image.save("captured_image.jpg")
            self.camera.configure(self.camera.create_preview_configuration(main={"size": (640, 400)}))
            
            
            messagebox.showinfo("Image Capture", "Image has been captured and saved as 'captured_image.jpg'")
        except Exception as e:
            messagebox.showerror("Capture Error", str(e))
    
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
            self.update_preview()

    def stop_camera(self):
        if self.camera:
            self.camera.stop()
            self.camera.close()
            self.camera = None
