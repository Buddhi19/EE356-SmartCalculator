import numpy as np
import sympy as sp
from main_controller import Calculator
import requests
from server_address import server_address
import re

class FourierSolver(Calculator):
    def __init__(self):
        super().__init__()
        self.x = sp.symbols("x")
        self.y = sp.symbols("y")
        self.t = sp.symbols("t")
        self.w = sp.symbols("w")
        self.pointer = 0
        self.result = ""
        self.showing_exp = "|"
        self.INVERSE = False

    def user_input(self, key):
        super().user_input(key)
        
    def convert_to_understandable(self):
        return super().convert_to_understandable()
    
    def final_expression(self):
        for key in self.mappings.keys():
            self.result = self.result.replace(key, self.mappings[key])

        if "e" in self.result:
            self.result = re.sub(r'e\^(\(.*?\))', r'exp(\1)', self.result)

        if "!" in self.result:
            try:
                index = self.result.index("!")
                # Extract the number preceding the "!"
                # Find the start of the number by looking backward until you hit a non-digit character
                start_index = index - 1
                while start_index >= 0 and self.result[start_index].isdigit():
                    start_index -= 1
                start_index += 1  # Move to the first digit of the number
                
                num = self.result[start_index:index]  # Extract the number
                self.result = self.result[:start_index] + "factorial(" + num + ")" + self.result[index+1:]
                print(self.result)
            except Exception as e:
                self.result = "factorial error"
                self.showing_exp = self.result
                return

        open_brackets = self.result.count("(")
        close_brackets = self.result.count(")")
        if open_brackets > close_brackets:
            self.result += ")" * (open_brackets - close_brackets)
        if self.result == "":
            self.showing_exp = "|"
            return
        print(f"Expression: {self.result}")
        if "^" in self.result:
            self.result = self.result.replace("^", "**")
        indicator = self.result[:self.pointer]+"|"+self.result[self.pointer:]
        return self.result


def get_fourier_transform(exp, t, w):
    url = server_address+'/fourier_transform_image'
    data = {'expression': exp, 'a': t, 'b': w}
    print(data)
    response = requests.post(url, json=data)
    if response.status_code == 200:
        with open('integrals/fourier_transform.png', 'wb') as f:
            f.write(response.content)
        print("Fourier transform image saved successfully.")
    else:
        print("Failed to generate Fourier transform image.")
    