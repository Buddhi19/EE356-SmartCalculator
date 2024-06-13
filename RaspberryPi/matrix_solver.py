import numpy as np
from main_controller import Calculator

class MatrixSolver(Calculator):
    def __init__(self, matA, matB, matC, matD, matE):
        super().__init__()
        self.matA = np.array(matA)
        self.matB = np.array(matB)
        self.matC = np.array(matC)
        self.matD = np.array(matD)
        self.matE = np.array(matE)
        self.result = ""
        self.showing_exp = "|"
        self.pointer = 0

    def linear_solver(self, expression):
        # Dictionary to map matrix names to actual matrices
        matrix_dict = {
            "matA": self.matA,
            "matB": self.matB,
            "matC": self.matC,
            "matD": self.matD,
            "matE": self.matE
        }

        # Replace matrix names in the expression with their actual values
        for key, value in matrix_dict.items():
            expression = expression.replace(key, f'matrix_dict["{key}"]')

        try:
            # Evaluate the expression with the matrices
            result = eval(expression)
            return result
        except Exception as e:
            return str(e)

    def user_input(self, key):
        matrix_dict = {
            "matA": self.matA,
            "matB": self.matB,
            "matC": self.matC,
            "matD": self.matD,
            "matE": self.matE
        }
        if key == "AC":
            self.result = ""
            self.showing_exp = "|"
            self.pointer = 0
        elif key == "DEL":
            if len(self.result) > 0:
                self.result = self.result[:self.pointer-1] + self.result[self.pointer:]
                self.pointer -= 1
                self.convert_to_understandable()
                return
            else:
                self.result = ""
                self.showing_exp = "|"
                self.pointer = 0
        elif key == "inv":
            if matrix_name in matrix_dict:
                try:
                    result = np.linalg.inv(matrix_dict[matrix_name])
                    self.result = str(result)
                except np.linalg.LinAlgError:
                    self.result = "Matrix is singular and cannot be inverted"
                except Exception as e:
                    self.result = f"Error: {str(e)}"
            else:
                self.result = "Unknown matrix"

        elif key == "=":
            open_brackets = self.result.count("(")
            close_brackets = self.result.count(")")
            if open_brackets > close_brackets:
                self.result += ")" * (open_brackets - close_brackets)
            if self.result == "":
                self.showing_exp = "|"
                return
            try:
                self.result = str(self.linear_solver(self.result))
            except ZeroDivisionError:
                self.result = "Cannot divide by zero"
            except SyntaxError:
                self.result = "Syntax error"
            except Exception as e:
                self.result = f"Error: {str(e)}"
            
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
            if self.pointer != 0 and key in self.functions:
                if self.result[self.pointer-1] not in self.operations:
                    self.result = self.result[:self.pointer] + "*" + self.keys[key] + self.result[self.pointer:]
                    self.pointer += 2
                    self.convert_to_understandable()
                    return
            self.result = self.result[:self.pointer] + self.keys[key] + self.result[self.pointer:]
            self.pointer += 1
            self.convert_to_understandable()
            return
        else:
            self.convert_to_understandable()
            return
        
    def convert_to_understandable(self):
        return super().convert_to_understandable()
    
if __name__ == "__main__": 
    matA = [[2, 3], [4, 5]]
    matB = [[1, 2], [3, 4]]
    matC = []
    matD = []
    matE = []
    mat = MatrixSolver(matA, matB, matC, matD, matE)
    matrix_name = "matA"  # Define the matrix name here
    mat.user_input("inv", matrix_name)  # Pass the matrix name to user_input
    print(mat.result)
    expression = "matA + matB"  # Define the expression here
    result = mat.linear_solver(expression)
    print(result)
