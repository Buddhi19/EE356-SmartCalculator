import tkinter as tk
from PIL import ImageGrab
import os

class WhiteboardApp(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Whiteboard App")
        self.pack(expand=True, fill=tk.BOTH)

        # Canvas for drawing
        self.canvas = tk.Canvas(self, bg='black', width=800, height=600)
        self.canvas.pack(expand=True, fill=tk.BOTH)

        # Buttons
        self.button_frame = tk.Frame(self)
        self.button_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.back_button = tk.Button(self.button_frame, text="Back", command=self.back)
        self.back_button.pack(side=tk.LEFT)

        self.erase_button = tk.Button(self.button_frame, text="Erase", command=self.erase)
        self.erase_button.pack(side=tk.LEFT)

        self.calculate_button = tk.Button(self.button_frame, text="Calculate", command=self.calculate)
        self.calculate_button.pack(side=tk.LEFT)

        self.plot_button = tk.Button(self.button_frame, text="Plot", command=self.plot)
        self.plot_button.pack(side=tk.LEFT)

        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw)

        self.lines = []
        self.current_line = []
        self.prev_x = None
        self.prev_y = None

    def start_draw(self, event):
        self.prev_x = event.x
        self.prev_y = event.y
        self.current_line = []

    def draw(self, event):
        if self.prev_x is not None and self.prev_y is not None:
            line = self.canvas.create_line(self.prev_x, self.prev_y, event.x, event.y, fill='white', width=5)
            self.current_line.append(line)
            self.prev_x = event.x
            self.prev_y = event.y
        if self.current_line not in self.lines:
            self.lines.append(self.current_line)

    def back(self):
        if self.lines:
            line = self.lines.pop()
            for segment in line:
                self.canvas.delete(segment)
            self.prev_x = None
            self.prev_y = None

    def erase(self):
        self.canvas.delete("all")
        self.lines = []
        self.current_line = []
        self.prev_x = None
        self.prev_y = None

    def save_as_image(self):
        # Update the canvas to make sure we capture everything
        self.canvas.update()

        # Get the root coordinates
        x = self.master.winfo_rootx()
        y = self.master.winfo_rooty()
        w = self.master.winfo_width()
        h = self.master.winfo_height()

        print(f"Coordinates: ({x}, {y}, {x + w}, {y + h})")  # Debugging print

        # Capture the root window content and save as an image
        image_path = os.path.join(os.getcwd(), "whiteboard.png")
        ImageGrab.grab(bbox=(x, y, x + w, y + h)).save(image_path)
        print(f"Image saved at {image_path}")  # Debugging print

    def calculate(self):
        self.save_as_image()

    def plot(self):
        self.save_as_image()
        # No additional action needed

if __name__ == "__main__":
    root = tk.Tk()
    app = WhiteboardApp(master=root)
    app.mainloop()
