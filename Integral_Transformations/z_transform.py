import sympy as sp

def sample(y_str, n, sig_len):
    y = sp.sympify(y_str)
    sig_array = [y.subs(n, i) for i in range(sig_len)]
    return sig_array

def z_transform(signal):
    z = sp.symbols('z')
    X_z = sum(signal[i] * z**(-i) for i in range(len(signal)))
    return sp.simplify(X_z)

if __name__ == "__main__":
    n = sp.symbols('n')
    y_str = 'n'  # Define the function as a string
    sig_len = 10  # Define the length of the signal
    signal = sample(y_str, n, sig_len)
    X_z = z_transform(signal)
    print(X_z)
