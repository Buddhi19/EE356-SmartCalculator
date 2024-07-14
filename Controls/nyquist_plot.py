import numpy as np
import matplotlib.pyplot as plt
from control import tf, nyquist_plot

def draw_nyquist_plot(numerator, denominator):
    # Create the transfer function
    system = tf(numerator, denominator)

    # Plot the root locus
    plt.figure()
    nyquist_plot(system)
    plt.title('Nyquist Plot')
    plt.xlabel('Real Axis')
    plt.ylabel('Imaginary Axis')
    plt.grid(True)
    plt.savefig('nyquist_plot.png')
    plt.show()

if __name__ == "__main__":
    # Example Transfer Function
    numerator = [1, 2]  # Coefficients of the numerator
    denominator = [1, 3, 2]  # Coefficients of the denominator

    draw_nyquist_plot(numerator, denominator)

