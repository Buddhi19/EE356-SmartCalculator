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

    def user_input(self, key):
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
        elif key == "plot":
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
                return
            
            x,y,z = sp.symbols("x y z")

            if "z" in self.result:
                self.plot_3d(self.result)
                return
            else:
                f, g = self.result.split("=")
                equation = sp.Eq(f,g)
                solve_y = sp.solve(equation, self.y)[0]
                x_vals = np.linspace(-self.range, self.range, 100)
                y_vals = sp.lambdify(self.x, solve_y, "numpy")(x_vals)
                plt.plot(x_vals, y_vals)
                plt.xlabel("x-axis")
                plt.ylabel("y-axis")
                plt.show()
                return

        elif key in self.keys:
            self.result = self.result[:self.pointer] + self.keys[key] + self.result[self.pointer:]
            self.pointer += 1

        else:
            return
        
    def plot_3d(self, z):
        f, g = z.split("=")
        equation = sp.Eq(f,g)
        solve_z = sp.solve(equation, z)[0]


        x_vals = np.linspace(-self.range, self.range, 100)
        y_vals = np.linspace(-self.range, self.range, 100)
        x_vals, y_vals = np.meshgrid(x_vals, y_vals)

        z_vals = sp.lambdify((self.x, self.y), solve_z,"numpy")(x_vals, y_vals)

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(x_vals, y_vals, z_vals, cmap="viridis")

        ax.set_xlabel("x-axis")
        ax.set_ylabel("y-axis")
        ax.set_zlabel("z-axis")

        plt.show()



if __name__ == "__main__":
    grapher = Grapher()
    while True:
        key = input("Enter key: ")
        grapher.user_input(key)
        