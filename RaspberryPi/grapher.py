import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from main_controller import Calculator

class Grapher(Calculator):
    def __init__(self):
        super().__init__()
        self.x = sp.symbols("x")
        self.y = sp.symbols("y")    
        self.z = sp.symbols("z")
        self.range = 10
        self.pointer = 0
        self.result = ""
        self.showing_exp = "|"

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
                
                from sympy.abc import x, y, z

                if "z" in self.result:
                    f, g = self.result.split("=")
                    equation = f + "-" + g
                    solve_z = sp.solve(equation, z)[0]

                    x_vals = np.linspace(-self.range, self.range, 100)
                    y_vals = np.linspace(-self.range, self.range, 100)
                    x_vals, y_vals = np.meshgrid(x_vals, y_vals)
                    z_vals = sp.lambdify((self.x, self.y), solve_z,"numpy")(x_vals, y_vals)
                    # fig = plt.figure()
                    # ax = fig.add_subplot(111, projection='3d')
                    # ax.plot_surface(x_vals, y_vals, z_vals, cmap="viridis")
                    # ax.set_xlabel("x-axis")
                    # ax.set_ylabel("y-axis")
                    # ax.set_zlabel("z-axis")
                    # plt.show()
                    return {"3D":[x_vals, y_vals, z_vals]}
                else:
                    f, g = self.result.split("=")
                    equation = f + "-" + g
                    print(equation)
                    solve_y = sp.solve(equation, y)[0]
                    x_vals = np.linspace(-self.range, self.range, 100)
                    y_vals = sp.lambdify(self.x, solve_y, "numpy")(x_vals)
                    # plt.plot(x_vals, y_vals)
                    # plt.xlabel("x-axis")
                    # plt.ylabel("y-axis")
                    # plt.show()
                    return {"2D":[x_vals, y_vals]}
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
    grapher = Grapher()
    while True:
        key = input("Enter key: ")
        grapher.user_input(key)
        indicator = grapher.result[:grapher.pointer]+"|"+grapher.result[grapher.pointer:]
        print(indicator)
        