import numpy as np
import matplotlib.pyplot as plt
from control import tf, root_locus

def draw_root_locus(numerator, denominator):
    # Create the transfer function
    system = tf(numerator, denominator)

    # Plot the root locus
    plt.figure()
    root_locus(system)
    plt.title('Root Locus')
    plt.xlabel('Real Axis')
    plt.ylabel('Imaginary Axis')
    plt.grid(True)
    plt.savefig('root_locus_plot.png')
    plt.show()

if __name__ == "__main__":
    # Example Transfer Function
    numerator = [1, 2]  # Coefficients of the numerator
    denominator = [1, 3, 2]  # Coefficients of the denominator

    draw_root_locus(numerator, denominator)

