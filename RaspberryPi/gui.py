import tkinter as tk

#scientific calculator gui

class CalculatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("iPhone Calculator with Round Buttons")
        self.geometry("800x480")
        self.configure(bg="black")
        
        self.expression = ""
        
        self.create_widgets()
    
    def create_widgets(self):
        # Create display widget
        self.display = tk.Entry(self, font=("Arial", 24), bg="black", fg="white", bd=0, justify='right')
        self.display.grid(row=0, column=0, columnspan=4, padx=10, pady=20, sticky='we')
        
        # Button layout
        buttons = [
            ('C', 1, 0, 'gray'), ('±', 1, 1, 'gray'), ('%', 1, 2, 'gray'), ('/', 1, 3, 'orange'),
            ('7', 2, 0, 'darkgray'), ('8', 2, 1, 'darkgray'), ('9', 2, 2, 'darkgray'), ('*', 2, 3, 'orange'),
            ('4', 3, 0, 'darkgray'), ('5', 3, 1, 'darkgray'), ('6', 3, 2, 'darkgray'), ('-', 3, 3, 'orange'),
            ('1', 4, 0, 'darkgray'), ('2', 4, 1, 'darkgray'), ('3', 4, 2, 'darkgray'), ('+', 4, 3, 'orange'),
            ('0', 5, 0, 'darkgray'), ('.', 5, 1, 'darkgray'), ('=', 5, 2, 'orange')
        ]
        
        # Create and place buttons
        for (text, row, col, color) in buttons:
            if text == '0':
                self.create_round_button(text, row, col, columnspan=2, color=color)
            else:
                self.create_round_button(text, row, col, color=color)
    
    def create_round_button(self, text, row, col, columnspan=1, color='white'):
        #import image as button background
        img = tk.PhotoImage(file="button.png").subsample(2, 2)
        button = tk.Button(self, text=text, image=img, compound=tk.CENTER, font=("Arial", 20), bg=color, fg="white", bd=0, command=lambda char=text: self.on_button_click(char))
        button.grid(row=row, column=col, columnspan=columnspan, padx=5, pady=5, sticky='we')

        for i in range(4):
            self.grid_columnconfigure(i, weight=1)
        for i in range(6):
            self.grid_rowconfigure(i, weight=1)
    
    def on_button_click(self, char):
        if char == '=':
            try:
                self.expression = str(eval(self.expression))
            except:
                self.expression = "Error"
        elif char == 'C':
            self.expression = ""
        elif char == '±':
            if self.expression:
                if self.expression[0] == '-':
                    self.expression = self.expression[1:]
                else:
                    self.expression = '-' + self.expression
        elif char == '%':
            try:
                self.expression = str(eval(self.expression) / 100)
            except:
                self.expression = "Error"
        else:
            self.expression += str(char)
        
        self.display.delete(0, tk.END)
        self.display.insert(tk.END, self.expression)

if __name__ == "__main__":
    app = CalculatorApp()
    app.mainloop()