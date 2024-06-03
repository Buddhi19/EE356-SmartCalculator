# This is the raspberry pi main controller script for calculator
import sympy as sp
class Calculator:
    def __init__(self):
        self.prev_expression = ""
        self.pointer = len(self.prev_expression)
        self.result = ""
        self.keys = {
            "0": "0", "1": "1", "2": "2", "3": "3", "4": "4",
            "5": "5", "6": "6", "7": "7", "8": "8", "9": "9",
            "+": "+", "-": "-", "*": "*", "/": "/", "(": "(",
            ")": ")", "=": "=", ".": ".", "x": "x","y": "y","z": "z",
            "sin": "S", "cos": "C", "tan": "T", "AC": "AC",
            "DEL": "DEL", "log": "L", "ln": "E", "sqrt": "R",
            "^": "^", "pi": "p", "e": "e",
            "arcsine": "aS", "arccos": "aC", "arctan": "aT"
        }
        self.mappings = {
            "S":"sin(", "C":"cos(", "T":"tan(", "L":"log(", "E":"ln(", "R":"sqrt(", "p":"pi",
            "aS":"asin(", "aC":"acos(", "aT":"atan("
        }
        self.operations = ["+", "-", "*", "/", "^", "S", "C", "T", "L", "E", "R", "p", "aS", "aC", "aT"]

        self.functions = ["sin", "cos", "tan", "log", "ln", "sqrt"]

        self.degrees = True

        self.mappings_for_degrees = {
            "S":"sin(pi/180*", "C":"cos(pi/180*", "T":"tan(pi/180*",
            "aS":"180/pi*asin(", "aC":"180/pi*acos(", "aT":"180/pi*atan(",
        }

    def update_pointer(self):
        self.pointer = len(self.result)

    def user_input(self,key):
        if key == "AC":
            self.result = ""
            self.pointer = 0
        elif key == "DEL":
            if len(self.result) > 0:
                self.result = self.result[:self.pointer-1] + self.result[self.pointer:]
                self.pointer -= 1
                return
            else:
                self.result = ""
                self.pointer = 0
        elif key == "=":
            if self.degrees:
                for key in self.mappings_for_degrees.keys():
                    self.result = self.result.replace(key, self.mappings_for_degrees[key])
            else:
                for key in self.mappings.keys():
                    self.result = self.result.replace(key, self.mappings[key])

            open_brackets = self.result.count("(")
            close_brackets = self.result.count(")")
            if open_brackets > close_brackets:
                self.result += ")" * (open_brackets - close_brackets)
            if self.result == "":
                return
            print(self.result)
            try:
                self.result = str(sp.sympify(self.result).evalf())
            except ZeroDivisionError:
                self.result = "Can not divide by zero"
            except SyntaxError:
                self.result = "Syntax error"
            except:
                self.result = "Error"
            print(self.result)

        elif key == "left":
            if self.pointer > 0:
                self.pointer -= 1
            if self.pointer == 0:
                self.pointer = len(self.result)
            return
        elif key == "right":
            if self.pointer < len(self.result):
                self.pointer += 1
            if self.pointer == len(self.result):
                self.pointer = 0
            return

        elif key in self.keys:
            print("line", self.pointer, self.result, key)
            if self.pointer !=0 and key in self.functions:
                if self.result[self.pointer-1] not in self.operations:
                    self.result = self.result[:self.pointer] +"*"+ self.keys[key] + self.result[self.pointer:]
                    self.pointer += 2
                    return
            self.result = self.result[:self.pointer] + self.keys[key] + self.result[self.pointer:]
            self.pointer += 1
        
        else:
            return

if __name__ == "__main__":
    Cal = Calculator()
    while True:
        key = input("Enter key: ")
        Cal.user_input(key)
        print(Cal.result, Cal.pointer)

        

            