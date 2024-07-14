import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
import latex2sympy2 as l2s2
from sympy.parsing.latex import parse_latex
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def convert_to_sympy(expression:str):
    """
    convert the given latex string to sympy 
    expression
    """
    return l2s2.latex2sympy(expression)



def plot_and_save(exp: str):
    f, g = exp.split("=")
    equation = f + "-" + g
    exp = convert_to_sympy(equation)
    print(exp)
    
    from sympy.abc import x, y, z
    
    plt.style.use('dark_background')  # Set the plot style to dark background
    
    if "z" in str(exp):
        print("3D plot")
        solve_z = sp.solve(exp, z)[0]
        x_vals = np.linspace(-10, 10, 100)
        y_vals = np.linspace(-10, 10, 100)
        x_vals, y_vals = np.meshgrid(x_vals, y_vals)
        z_vals = sp.lambdify((x, y), solve_z, "numpy")(x_vals, y_vals)

        fig = plt.figure(figsize=(4.3, 6), dpi=100, facecolor="black")
        ax = fig.add_subplot(111, projection='3d')
        
        ax.plot_surface(x_vals, y_vals, z_vals, cmap="viridis", edgecolor='none')

        ax.set_facecolor("black")
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        ax.tick_params(axis='z', colors='white')
        ax.yaxis.label.set_color('white')
        ax.xaxis.label.set_color('white')
        ax.zaxis.label.set_color('white')
        ax.xaxis.pane.fill = False
        ax.yaxis.pane.fill = False
        ax.zaxis.pane.fill = False
        plt.savefig("result_plot.png")
        plt.close(fig)
    else:
        print("2D plot")
        solve_y = sp.solve(exp, y)[0]
        x_vals = np.linspace(-10, 10, 100)
        y_vals = sp.lambdify(x, solve_y, "numpy")(x_vals)

        fig = plt.figure(figsize=(4.3, 6), dpi=100, facecolor="black")
        ax = fig.add_subplot(111)
        ax.plot(x_vals, y_vals)
        ax.set_facecolor("black")
        ax.spines['bottom'].set_color('white')
        ax.spines['left'].set_color('white')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        ax.yaxis.label.set_color('white')
        ax.xaxis.label.set_color('white')
        plt.savefig("result_plot.png")
        plt.close(fig)  # Close the figure to release memory

    return (os.path.abspath("result_plot.png"))


if __name__ == '__main__':
    exp = r"z=x^2+y^2"
    print(plot_and_save(exp))