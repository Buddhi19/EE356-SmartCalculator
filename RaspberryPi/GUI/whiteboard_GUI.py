import tkinter as tk
from tkinter import messagebox
from PIL import ImageGrab

class WhiteboardApp(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        self.canvas = tk.Canvas(self, bg="black")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.reset_coords)

        self.erase_button = tk.Button(self, text="Erase", command=self.erase)
        self.erase_button.pack(side=tk.LEFT)

        self.back_button = tk.Button(self, text="Back", command=self.back)
        self.back_button.pack(side=tk.LEFT)

        self.calculate_button = tk.Button(self, text="Calculate", command=self.calculate)
        self.calculate_button.pack(side=tk.RIGHT)

        self.plot_button = tk.Button(self, text="Plot", command=self.plot)
        self.plot_button.pack(side=tk.RIGHT)

        self.previous_coords = None

    def draw(self, event):
        if self.previous_coords:
            x1, y1 = self.previous_coords
            x2, y2 = event.x, event.y
            self.canvas.create_line(x1, y1, x2, y2, fill="white", width=5, capstyle=tk.ROUND)
        self.previous_coords = event.x, event.y

    def erase(self):
        self.canvas.delete("all")

    def back(self):
        # Add code to go back to the previous page
        pass

    def calculate(self):
        self.save_whiteboard("calculate.png")
        # Add code for calculations here

    def plot(self):
        self.save_whiteboard("plot.png")
        # Add code for plotting here

    def save_whiteboard(self, filename):
        x0 = self.canvas.winfo_rootx() + self.canvas.winfo_x()
        y0 = self.canvas.winfo_rooty() + self.canvas.winfo_y()
        x1 = x0 + self.canvas.winfo_width()
        y1 = y0 + self.canvas.winfo_height()
        ImageGrab.grab().crop((x0, y0, x1, y1)).save(filename)

    def reset_coords(self, event):
        self.previous_coords = None

# Example usage:
if __name__ == "__main__":
    root = tk.Tk()
    app = WhiteboardApp(root, None)
    app.pack(fill=tk.BOTH, expand=True)
    root.mainloop()
