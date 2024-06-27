import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from sympy import I
import time

class Laplace:
    def __init__(self, expression: str, a: str, b: str):
        self.expression = expression
        self.a = a
        self.b = b
        self.t = sp.symbols(a)
        self.s = sp.symbols(b)
        self.expression = sp.sympify(expression)
        self.laplace_transform = self.get_laplace_transform()
        self.get_equation_image(self.laplace_transform)
        self.plot_spectrums()

    def get_laplace_transform(self):
        laplace_transform = sp.laplace_transform(self.expression, self.t, self.s, noconds=True)
        ans = sp.simplify(laplace_transform)
        return ans

    def get_equation_image(self, expression):
        if isinstance(expression, sp.Piecewise):
            latex_expression = r"\begin{cases}"
            for expr, cond in expression.args:
                latex_expression += r"%s & \text{if } %s \\" % (sp.latex(expr), sp.latex(cond))
            latex_expression += r"\end{cases}"
        else:
            latex_expression = sp.latex(expression)
        
        FONT_SIZE = 24
        if len(latex_expression) > 100:
            FONT_SIZE = 18
        if len(latex_expression) > 200:
            FONT_SIZE = 11

        plt.figure(figsize=(4.3, 2), dpi=100, facecolor='black')
        plt.text(0.5, 0.5, r"$%s$" % latex_expression, fontsize=FONT_SIZE, ha='center', va='center', color='white')
        plt.axis('off')
        plt.savefig("laplace_transform.png")
        plt.show()
        time.sleep(0.5)
        plt.close()

    def plot_spectrums(self):
        w = np.linspace(-100, 100, 1000)
        s = 1j * w
        laplace_func = sp.lambdify(self.s, self.laplace_transform, 'numpy')
        H = laplace_func(s)

        magnitude = np.abs(H)
        phase = np.angle(H)

        plt.figure(figsize=(4.3, 6), facecolor='black')

        ax1 = plt.subplot(2, 1, 1, facecolor='black')
        ax1.plot(w, magnitude)
        ax1.set_title('Magnitude Response', color='white')
        ax1.set_xlabel('Frequency (rad/s)', color='white')
        ax1.set_ylabel('Magnitude', color='white')
        ax1.grid(True, color='gray')
        ax1.tick_params(colors='white')

        ax2 = plt.subplot(2, 1, 2, facecolor='black')
        ax2.plot(w, phase)
        ax2.set_title('Phase Response', color='white')
        ax2.set_xlabel('Frequency (rad/s)', color='white')
        ax2.set_ylabel('Phase', color='white')
        ax2.grid(True, color='gray')
        ax2.tick_params(colors='white')

        plt.tight_layout()
        plt.savefig("laplace_spectrum.png")
        plt.show()
        time.sleep(0.5)
        plt.close()


if __name__ == "__main__":
    expression = "sin(2*pi*60*t)"
    a = "t"
    b = "s"
    laplace = Laplace(expression, a, b)
