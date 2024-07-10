import sympy as sp

def z_transform(signal, n):
    z = sp.symbols('z')
    
    X_z = sum(signal[i] * z**(-i) for i in range(len(signal)))
    
    return sp.simplify(X_z)

if __name__ == "__main":
    n = sp.symbols('n')
    signal = [1, 2, 3, 4]

    X_z = z_transform(signal, n)
    print(X_z)

    