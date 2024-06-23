import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from scipy import signal
import sys
import os

parent_dir = os.path.dirname(os.path.abspath(__file__))

def save_bode_plot(numerator,denominator):
    s = sp.symbols("s")
    poly_numerator = sp.Poly(numerator, s)
    numerator_coefficients = poly_numerator.all_coeffs()
    numerator_coefficients = [float(coef) for coef in numerator_coefficients]

    poly_denominator = sp.Poly(denominator, s)
    denominator_coefficients = poly_denominator.all_coeffs()
    denominator_coefficients = [float(coef) for coef in denominator_coefficients]

    transfer_function = signal.TransferFunction(numerator_coefficients, denominator_coefficients)
    w, mag, phase = signal.bode(transfer_function)

    #plot in black background name axis and title for both plots
    fig, ax = plt.subplots(2, 1)
    ax[0].plot(w, mag)
    ax[0].set_xscale('log')
    ax[0].set_title('Magnitude Plot')
    ax[0].set_ylabel('Magnitude (dB)')
    ax[0].set_xlabel('Frequency (rad/s)')
    ax[0].grid()

    ax[1].plot(w, phase)
    ax[1].set_xscale('log')
    ax[1].set_title('Phase Plot')
    ax[1].set_ylabel('Phase (degrees)')
    ax[1].set_xlabel('Frequency (rad/s)')
    ax[1].grid()
    
    plt.savefig(os.path.join(parent_dir, "bode_plot.png"))
    plt.show()
    return os.path.join(parent_dir, "bode_plot.png")

def save_nyquist_plot(numerator,denominator):
    s = sp.symbols("s")
    poly_numerator = sp.Poly(numerator, s)
    numerator_coefficients = poly_numerator.all_coeffs()
    numerator_coefficients = [float(coef) for coef in numerator_coefficients]

    poly_denominator = sp.Poly(denominator, s)
    denominator_coefficients = poly_denominator.all_coeffs()
    denominator_coefficients = [float(coef) for coef in denominator_coefficients]

    transfer_function = signal.TransferFunction(numerator_coefficients, denominator_coefficients)
    w, h = signal.freqresp(transfer_function)

    fig, ax = plt.subplots()
    ax.plot(h.real, h.imag)
    ax.set_title('Nyquist Plot')
    ax.set_ylabel('Imaginary')
    ax.set_xlabel('Real')
    ax.grid()
    
    plt.savefig(os.path.join(parent_dir, "nyquist_plot.png"))
    plt.show()
    return os.path.join(parent_dir, "nyquist_plot.png")

def save_root_locus_plot(numerator,denominator):
    s = sp.symbols("s")
    poly_numerator = sp.Poly(numerator, s)
    numerator_coefficients = poly_numerator.all_coeffs()
    numerator_coefficients = [float(coef) for coef in numerator_coefficients]

    poly_denominator = sp.Poly(denominator, s)
    denominator_coefficients = poly_denominator.all_coeffs()
    denominator_coefficients = [float(coef) for coef in denominator_coefficients]

    pass

if __name__ == "__main__":
    num = input()
    den = input()
    save_bode_plot(num, den)
    save_nyquist_plot(num, den)
    save_root_locus_plot(num, den)