import numpy as np
import sympy as sp
from main_controller import Calculator
import requests

class FourierSolver(Calculator):
    def __init__(self):
        super().__init__()
        self.x = sp.symbols("x")
        self.y = sp.symbols("y")
        self.t = sp.symbols("t")
        self.w = sp.symbols("w")
        self.pointer = 0
        self.result = ""
        self.showing_exp = "|"
        self.INVERSE = False

    def user_input(self, key):
        super().user_input(key)
        
    def convert_to_understandable(self):
        return super().convert_to_understandable()