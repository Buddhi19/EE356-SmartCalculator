import latex2sympy2 as l2s2
import sympy as sp
import numpy as np

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
    

# if __name__ == '__main__':
#     exp = r"\frac{d}{dx}x^2+x"
#     cal = Cal()
#     print(cal.differentiator(exp))
