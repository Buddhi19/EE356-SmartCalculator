import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from sympy import preview
import time
from scipy.fftpack import fft, fftfreq

class Fourier:
    def __init__(self, expression:str, a:str, b:str):
        self.expression = expression
        self.a = a
        self.b = b
        self.t = sp.symbols(a)
        self.w = sp.symbols(b)
        self.expression = sp.sympify(expression)
        self.fourier_transform = self.get_fourier_transform()
        self.get_equation_image(self.fourier_transform)
        self.plot_spectrums()

    def get_fourier_transform(self):
        fourier_transform = sp.fourier_transform(self.expression, self.t, self.w)
        ans = sp.simplify(fourier_transform)
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
        plt.savefig("fourier_transform.png")
        plt.show()
        time.sleep(0.5)
        plt.close()


    def plot_spectrums(self):
        expr_func = sp.lambdify(self.t, self.expression, 'numpy')
        
        t_vals = np.linspace(-10, 10, 1000)
        sample_rate = t_vals[1] - t_vals[0]
        # print(sample_rate)
        
        y_vals = expr_func(t_vals)
        
        yf = fft(y_vals)
        xf = fftfreq(len(t_vals), sample_rate)
        
        yf = np.fft.fftshift(yf)
        xf = np.fft.fftshift(xf)
        
        magnitude = np.abs(yf)
        # normalize the magnitude
        magnitude = magnitude / np.max(magnitude)
        phase = np.angle(yf)
        
        plt.figure(figsize=(4.3, 6), facecolor='black')
        
        ax1 = plt.subplot(2, 1, 1, facecolor='black')
        ax1.plot(xf, magnitude)
        ax1.set_title('Magnitude Response', color='white')
        ax1.set_xlabel('Frequency', color='white')
        ax1.set_ylabel('Magnitude', color='white')
        ax1.grid(True, color='gray')
        ax1.tick_params(colors='white')
        
        
        ax2 = plt.subplot(2, 1, 2, facecolor='black')
        ax2.plot(xf, phase)
        ax2.set_title('Phase Response', color='white')
        ax2.set_xlabel('Frequency', color='white')
        ax2.set_ylabel('Phase', color='white')
        ax2.grid(True, color='gray')
        ax2.tick_params(colors='white')
        
        plt.tight_layout()
        plt.savefig("fourier_spectrum.png")
        plt.show()


if __name__ == "__main__":
    expression = "sin(2*pi*10*t)"
    a = "t"
    b = "w"
    fourier = Fourier(expression, a, b)