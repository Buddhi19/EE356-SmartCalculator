import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
import latex2sympy2 as l2s2

def convert_to_sympy(expression:str):
    """
    convert the given latex string to sympy 
    expression
    """
    return l2s2.latex2sympy(expression)

def plot_and_save(exp:str):
    """
    draw the graph and save it as an image
    """
    x = sp.symbols('x')
    y = convert_to_sympy(exp)

    x_vals = np.linspace(-10, 10, 100)
    y_vals = [y.subs(x, val) for val in x_vals]

    plt.plot(x_vals, y_vals)
    plt.xlabel('x-axis')
    plt.ylabel('y-axis')
    plt.grid(True)
    plt.title(exp)
    plt.savefig('result.png')

# if __name__ == '__main__':
#     exp = r"\frac{1}{1 + e^{-x}}"
#     plot_and_save(exp)
