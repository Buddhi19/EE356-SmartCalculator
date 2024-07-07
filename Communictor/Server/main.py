import os
import sys

sys.path.append(os.path.dirname("../../"))

from Latex_Extractor.main import Image2Text, convert_blackboard_image
from Calculator.main import Cal
import cv2
from Controls.main import save_bode_plot
from Integral_Transformations.fourier import Fourier
from Integral_Transformations.laplace import Laplace

def process_image(img_location):
    I2T = Image2Text()
    img = cv2.imread(img_location)
    cv2.imshow("img",img)
    cv2.waitKey(1000)
    return(I2T.run_for_std_scenario(img))

def process_image_for_whiteboard(img_location):
    I2T = Image2Text()
    img = cv2.imread(img_location)
    cv2.imshow("img",img)
    cv2.waitKey(0)
    im2 = convert_blackboard_image(img)
    return(I2T.run_for_training_scenario(im2))

def calculate_expression(expression):
    if not expression:
        return []
    cal = Cal()
    ans = []
    for exp in expression:
        ans.append(cal.do_nothing(exp))

    return ans

def save_bode_plot_from_image(numerator,denominator):
    path = save_bode_plot(numerator,denominator)
    return path

def fourier_solver(expression,a,b):
    fourier = Fourier(expression,a,b)
    return fourier.fourier_transform

def fourier_transform_image():
    path = "fourier_spectrum.png"
    return path

def fourier_equation_image():
    path = "fourier_transform.png"
    return path

def laplace_solver(expression,a,b):
    laplace = Laplace(expression,a,b)
    return laplace.laplace_transform

def laplace_equation_image():
    path = "laplace_transform.png"
    return path

def laplace_spectrum_image():
    path = "laplace_spectrum.png"
    return path