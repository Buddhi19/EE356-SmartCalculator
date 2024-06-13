import numpy as np
from main_controller import Calculator
import numpy as np

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
        matrix_dict = {
            "MatA": self.matA,
            "MatB": self.matB,
            "MatC": self.matC,
            "MatD": self.matD,
            "MatE": self.matE
        }
        for key, value in matrix_dict.items():
            expression = expression.replace(key, f'matrix_dict["{key}"]')

        # Evaluate the expression safely
        return eval(expression, {"__builtins__": None}, {"matrix_dict": matrix_dict, "np": np})

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
                print(self.result)
                print(self.matA)
                self.result = str(self.linear_solver(self.result))
            except ZeroDivisionError:
                self.result = "Cannot divide by zero"
            except SyntaxError:
                self.result = "Syntax error"
            except Exception as e:
                self.result = f"Error: {e}"
            
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
    
    def update_matrix(self, MatA, MatB, MatC, MatD, MatE):
        self.matA = np.array(MatA)
        self.matB = np.array(MatB)
        self.matC = np.array(MatC)
        self.matD = np.array(MatD)
        self.matE = np.array(MatE)

# Example matrices for testing
if __name__ == "__main__":
    import numpy as np
    matA = np.array([[1, 2], [3, 4]])
    matB = np.array([[5, 6], [7, 8]])
    matC = np.array([[9, 10], [11, 12]])
    matD = np.array([[13, 14], [15, 16]])
    matE = np.array([[17, 18], [19, 20]])

    solver = MatrixSolver(matA, matB, matC, matD, matE)
    print(solver.linear_solver("MatA * 8"))
