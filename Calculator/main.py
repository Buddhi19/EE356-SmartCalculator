import latex2sympy2 as l2s2
import sympy as sp
import numpy as np

def convert_to_sympy(expression:str):
    """
    convert latex to sympy expression
    """
    return l2s2.latex2sympy(expression)

def calculate(expression:str):
    """
    calculate the given expression
    """
    ans = convert_to_sympy(expression)
    print(float(ans))

# if __name__ == '__main__':
#     exp = r"\frac{1345+987}{100}"
#     calculate(exp)
