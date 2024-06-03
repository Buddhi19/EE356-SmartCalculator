# This is the raspberry pi main controller script for calculator
import sympy as sp


class Calculator:
    def __init__(self):
        self.prev_expression = ""
        self.result = ""
        self.keys = {
            "0": "0", "1": "1", "2": "2", "3": "3", "4": "4",
            "5": "5", "6": "6", "7": "7", "8": "8", "9": "9",
            "+": "+", "-": "-", "*": "*", "/": "/", "(": "(",
            ")": ")", "C": "C", "=": "=", ".": ".", "x": "x",
            "sin": "sin(", "cos": "cos(", "tan": "tan(", "AC": "AC",
            "DEL": "DEL", "log": "log", "ln": "ln(", "sqrt": "sqrt(",
            "^": "^", "pi": "pi", "e": "e"
        }

    def user_input(self,key):
        if key == "AC":
            self.result = ""
        elif key == "DEL":
            if len(self.result) > 0:
                self.result = self.result[:-1]
            else:
                self.result = ""
        elif key == "=":
            open_brackets = self.result.count("(")
            close_brackets = self.result.count(")")
            if open_brackets > close_brackets:
                self.result += ")" * (open_brackets - close_brackets)
            if self.result == "":
                return
            try:
                self.result = str(sp.sympify(self.result).evalf())
            except ZeroDivisionError:
                self.result = "Math error"
            except SyntaxError:
                self.result = "Syntax error"
            except:
                self.result = "Error"

            print(self.result)

        else:
            self.result += self.keys[key]


if __name__ == "__main__":
    Cal = Calculator()
    while True:
        key = input("Enter key: ")
        Cal.user_input(key)

        

            