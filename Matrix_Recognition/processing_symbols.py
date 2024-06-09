import cv2 as cv

class Symbol:
    def __init__(self, image, top_left, bottom_right, symbol):
        self.image = image
        self.top_left = top_left
        self.bottom_right = bottom_right
        self.symbol = symbol

    def is_left_square_bracket(self):
        return self.symbol == "["

    def __str__(self):
        return f"Symbol: {self.symbol}, Top-left: {self.top_left}, Bottom-right: {self.bottom_right}"

# Example image and coordinates
image = cv.imread('images/Matrix.png')
top_left = (10, 20)
bottom_right = (30, 50)
symbol = "3"

detected_symbol = Symbol(image, top_left, bottom_right, symbol)

# Check if the symbol is a left square bracket
is_left_bracket = detected_symbol.is_left_square_bracket()
print(f"Is the symbol a '['? {is_left_bracket}")

# Print the symbol details
print(detected_symbol)
