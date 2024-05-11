import latex2sympy2 as l2s2
import sympy as sp
import numpy as np
from sympy import re, im, I, E

class formatter:
    def __init__(self):
        self.convert_to_latex
        self.convert_to_sympy
    def convert_to_sympy(self,expression:str):
        """
        convert latex to sympy expression
        """
        return l2s2.latex2sympy(expression)

    def convert_to_latex(self,expression):
        """
        convert sympy expression to latex
        """
        return sp.latex(expression)

class Cal(formatter):
    def calculate(self, expression:str):
        """
        calculate the given expression
        """
        ans = self.convert_to_sympy(expression)
        return (self.convert_to_latex(float(ans)))

    def differentiator(self,expression:str):
        """
        differentiate the given expression
        """
        x, y, z, t = sp.symbols('x y z t')
        ans = self.convert_to_sympy(expression)
        return (self.convert_to_latex(sp.simplify(ans)))
    
    def integral(self,expression:str):
        """
        integrate the given expression
        """
        x, y, z, t = sp.symbols('x y z t')
        ans = self.convert_to_sympy(expression)
        return (self.convert_to_latex(sp.integrate(ans)))
    
    def limiter(self,expression:str):
        """
        limit the given expression
        """
        x, y, z, t = sp.symbols('x y z t')
        ans = self.convert_to_sympy(expression)
        return (self.convert_to_latex(sp.limit(ans)))
    
    def complex_calculator(self,expression:str):
        """
        calculate the complex expression
        """
        filtered_expression = ""
        for c in expression:
            if c!="i" and c!="j":
                filtered_expression += c
            else:
                filtered_expression += "I"
        print(filtered_expression)
        ans = self.convert_to_sympy(filtered_expression)
        ans = re(ans) + im(ans)*I
        return (self.convert_to_latex(ans))

if __name__ == '__main__':
    exp = r"\frac{1}{1+j}"
    cal = Cal()
    print(cal.complex_calculator(exp))
