# This is the raspberry pi main controller script for calculator
import sympy as sp
import math
class Calculator:
    def __init__(self):
        self.prev_expression = ""
        self.pointer = len(self.prev_expression)
        self.result = ""
        self.showing_exp = "|"
        self.keys = {
            "0": "0", "1": "1", "2": "2", "3": "3", "4": "4",
            "5": "5", "6": "6", "7": "7", "8": "8", "9": "9",
            "+": "+", "-": "-", "*": "*", "/": "/", "(": "(",
            ")": ")", "=": "=", ".": ".", "x": "x","y": "y","z": "z",
            "sin": "S", "cos": "C", "tan": "T", "AC": "AC",
            "DEL": "DEL", "log": "L", "ln": "E", "sqrt": "R",
            "^": "^", "pi": "p", "e": "e",
            "arcsine": "aS", "arccos": "aC", "arctan": "aT","i":"I"
        }
        self.mappings = {
            "S":"sin(", "C":"cos(", "T":"tan(", "L":"log(", "E":"ln(", "R":"sqrt(",
            "aS":"asin(", "aC":"acos(", "aT":"atan(","p":"pi", "I":"i"
        }
        self.operations = ["+", "-", "*", "/", "^", "S", "C", "T", "L", "E", "R", "p", "aS", "aC", "aT","="]

        self.functions = ["sin", "cos", "tan", "log", "ln", "sqrt", "pi", "arcsine", "arccos", "arctan","x","y","z","i"]

        self.degrees = True

        self.mappings_for_degrees = {
            "S":"sin(pi/180*", "C":"cos(pi/180*", "T":"tan(pi/180*",
            "aS":"180/pi*asin(", "aC":"180/pi*acos(", "aT":"180/pi*atan(","L":"log(,", "E":"ln(",
            "R":"sqrt(", "I":"i",
        }

    def safe_eval(self,expression):
        allowed_names = {
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'hypot': math.hypot,
            'log': math.log,
            'exp': math.exp,
            'sqrt': math.sqrt,
            'pi': math.pi,
            'p': math.pi,
            'e': math.e,
            'factorial': math.factorial,
            'asin': math.asin,
            'acos': math.acos,
            'atan': math.atan,
            'I': 1j,
            # Add more functions and constants as needed
        }

        code = compile(expression, "<string>", "eval")
        for name in code.co_names:
            if name not in allowed_names:
                raise NameError(f"Use of '{name}' not allowed")

        return eval(code, {"__builtins__": {}}, allowed_names)

    def update_pointer(self):
        self.pointer = len(self.result)

    def user_input(self,key):
        if key == "AC":
            self.result = ""
            self.showing_exp = "|"
            self.pointer = 0
        elif key == "DEL":
            if len(self.result) > 0 and self.pointer > 0:
                self.result = self.result[:self.pointer-1] + self.result[self.pointer:]
                self.pointer -= 1
                self.convert_to_understandable()
                return
            elif len(self.result) > 0 and self.pointer == 0:
                return
            else:
                self.result = ""
                self.pointer = 0
                self.showing_exp = "|"
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
                self.showing_exp = "|"
                return
            indicator = self.result[:self.pointer]+"|"+self.result[self.pointer:]
            try:
                self.result = str(self.safe_eval(self.result))
                if "j" in self.result:
                    self.result = self.result.replace("j","i")
            except ZeroDivisionError:
                self.result = "Can not divide by zero"
            except SyntaxError:
                self.result = "Syntax error"
            except:
                self.result = "Error"
            print(self.result)
            self.showing_exp = self.result
            return self.result

        elif key == "left":
            if self.pointer > 0:
                self.pointer -= 1
            if self.pointer == 0:
                self.pointer = len(self.result)
            self.convert_to_understandable()
            return
        elif key == "right":
            if self.pointer < len(self.result):
                self.pointer += 1
            if self.pointer == len(self.result):
                self.pointer = 0
            self.convert_to_understandable()
            return

        elif key in self.keys:
            print("line", self.pointer, self.result, key)
            if self.pointer !=0 and key in self.functions:
                if self.result[self.pointer-1] not in self.operations:
                    self.result = self.result[:self.pointer] +"*"+ self.keys[key] + self.result[self.pointer:]
                    self.pointer += 2
                    self.convert_to_understandable()
                    return
            self.result = self.result[:self.pointer] + self.keys[key] + self.result[self.pointer:]
            self.pointer += 1
            self.convert_to_understandable()
            return
        else:
            return
        
    def convert_to_understandable(self):
        for_show = self.result
        for_show = for_show[:self.pointer]+"|"+for_show[self.pointer:]
        for key in self.mappings.keys():
            if key in for_show:
                for_show = for_show.replace(key, self.mappings[key])
        for_show = for_show.replace("*","\u00D7")
        self.showing_exp = for_show

if __name__ == "__main__":
    Cal = Calculator()
    while True:
        key = input("Enter key: ")
        Cal.user_input(key)
        indicator = Cal.result[:Cal.pointer]+"|"+Cal.result[Cal.pointer:]
        print(indicator)

        

            