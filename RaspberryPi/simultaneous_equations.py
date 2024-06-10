import sympy as sp
import math

from main_controller import Calculator

class SimultaneousEquations:
    def __init__(self):
        pass
    def solve_equations(self,equations):
        parsed_equations = [sp.sympify(eq).evalf() for eq in equations]
        variables = list(set().union(*[eq.free_symbols for eq in parsed_equations]))

        solutions = sp.solve(parsed_equations, variables)

        return solutions
    
    def simultaneous_solver(self, equations):
        equations_simplified = []
        for eq in equations:
            f,g = eq.split("=")
            eq_simplified = f+"-"+g
            equations_simplified.append(eq_simplified)
        solutions = self.solve_equations(equations_simplified)
        return solutions
    

class Simul(Calculator):
    def __init__(self):
        super().__init__()
        self.pointer = 0
        self.result = ""
        self.showing_exp = "|"
        self.equations = []

    def user_input(self, key):
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
        elif key == "plot":
            try:
                if not self.degrees:
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
                self.equations.append(self.result)
                return
            except:
                self.result = "Error in the input"
                self.showing_exp = self.result
                return {"Error":self.result}
            
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
            self.convert_to_understandable()
            return
        
    def convert_to_understandable(self):
        return super().convert_to_understandable()


if __name__ == "__main__":
    equations = []

    # Input the number of equations
    num_equations = int(input("Enter the number of equations: "))

    # Input each equation
    for i in range(num_equations):
        eq = input(f"Enter equation {i + 1}: ")
        equations.append(eq)

    simul =SimultaneousEquations()
    # Solve the equations
    solutions = simul.solve_equations(equations)
    print(solutions)
    # Print the solutions
    if solutions:
        print("Solutions:")
        # Check the type of the solutions and handle accordingly
        if isinstance(solutions, dict):
            for var, val in solutions.items():
                print(f"{var} = {val}")
        elif isinstance(solutions, list):
            for sol in solutions:
                if isinstance(sol, dict):
                    for var, val in sol.items():
                        print(f"{var} = {val}")
                else:
                    print(sol)
        else:
            print(solutions)
    else:
        print("No solution found or infinite solutions exist.")
