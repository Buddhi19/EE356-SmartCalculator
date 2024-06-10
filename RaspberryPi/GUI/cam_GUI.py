import tkinter as tk
from tkinter import simpledialog, messagebox
from picamera import PiCamera
from PIL import Image, ImageTk
import io

class CameraApp(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.pack()
        self.create_widgets()
        self.camera = PiCamera()
        self.update_image()

    def create_widgets(self):
        self.img_label = tk.Label(self)
        self.img_label.pack()

        self.button_frame = tk.Frame(self)
        self.button_frame.pack(pady=10)

        self.capture_button = tk.Button(self.button_frame, text="Capture", command=self.capture_image)
        self.capture_button.grid(row=0, column=0, padx=5)

        self.back_button = tk.Button(self.button_frame, text="Back", command=self.back_action)
        self.back_button.grid(row=0, column=1, padx=5)

        self.send_button = tk.Button(self.button_frame, text="Send", command=self.send_action)
        self.send_button.grid(row=0, column=2, padx=5)

        self.mode_button = tk.Button(self.button_frame, text="Mode", command=self.select_mode)
        self.mode_button.grid(row=0, column=3, padx=5)

    def update_image(self):
        stream = io.BytesIO()
        self.camera.capture(stream, format='jpeg')
        stream.seek(0)
        image = Image.open(stream)
        image = image.resize((400, 300))
        photo = ImageTk.PhotoImage(image)
        self.img_label.config(image=photo)
        self.img_label.image = photo
        self.after(1000, self.update_image)

    def capture_image(self):
        self.camera.capture('captured_image.jpg')

    def select_mode(self):
        modes = ["calculate", "complex", "matrix", "equation", "plot"]
        mode = simpledialog.askstring("Select Mode", "Choose a mode:", initialvalue=modes[0], values=modes)
        if mode:
            messagebox.showinfo("Mode Selected", f"Mode selected: {mode}")

    def back_action(self):
        messagebox.showinfo("Back", "Back button pressed")

    def send_action(self):
        messagebox.showinfo("Send", "Send button pressed")

class ApplicationController:
    def __init__(self, root):
        self.root = root
        self.camera_app = CameraApp(parent=root, controller=self)
        self.camera_app.pack()

def main():
    root = tk.Tk()
    root.title("Raspberry Pi Camera Interface")
    app_controller = ApplicationController(root)
    root.mainloop()

if __name__ == "__main__":
    main()
