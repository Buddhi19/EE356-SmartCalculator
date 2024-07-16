import sympy as sp

def sample(y_str, n, sig_len):
    y = sp.sympify(y_str)
    sig_array = [y.subs(n, i) for i in range(sig_len)]
    return sig_array

def z_transform(expression):
    # Define the variable n and z
    n, z = sp.symbols('n z')
    
    # Ensure the input expression is a sympy expression
    if isinstance(expression, str):
        expression = sp.sympify(expression)
    
    # Compute the Z-transform
    try:
        Z_transform = sp.summation(expression * z**(-n), (n, 0, sp.oo))
    except TypeError as e:
        raise ValueError(f"Invalid expression: {expression}. Error: {e}")
    
    return Z_transform

if __name__ == "__main__":
    n = sp.symbols('n')
    y_str = 'n'  # Define the function as a string
    sig_len = 10  # Define the length of the signal
    signal = sample(y_str, n, sig_len)
    X_z = z_transform(signal)
    print(X_z)
