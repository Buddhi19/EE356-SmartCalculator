import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

import mathreader
from mathreader.api import *
from mathreader.image_processing import preprocessing, postprocessing
from mathreader.config import Configuration
from mathreader.helpers.exceptions import *
import cv2
import numpy as np
from PIL import ImageGrab
import imutils
import tensorflow as tf

configs = Configuration()

class Extractor:
    def __init__(self):
        expression = ""
        hme_recognizer = HME_Recognizer()
        print(f"location {sys.argv}")
    
        arr = os.listdir(os.path.join(current_dir))
        images = []
        for i in arr:
            if i.endswith('.png') or i.endswith('.jpg'):
                images.append(os.path.join(current_dir, i))

        cv2.imshow("test", cv2.imread(images[0]))
        cv2.waitKey(0)

        for image in images:

            try:
                hme_recognizer.load_image(image, data_type='path')
                expression, img = hme_recognizer.recognize()

                lex_errors = hme_recognizer.get_lex_errors()
                yacc_errors = hme_recognizer.get_yacc_errors()
                pure_lex_errors = hme_recognizer.get_lex_pure_errors()
                pure_yacc_errors = hme_recognizer.get_yacc_pure_errors()
                latex_string_original = hme_recognizer.get_latex_string_original()

                print('\n\nLex errors: ', lex_errors)
                print('\n\nYacc errors: ', yacc_errors)
                print('\n\nPure Lex Errors:', pure_lex_errors)
                print('\n\nPure Yacc Errors: ', pure_yacc_errors)
                print('\n\nOriginal Expression: ', latex_string_original)

            except (GrammarError, SintaticError, LexicalError) as e:

                if 'latex_string_original' in e.data:
                    expression = e.data['latex_string_original']

                print('[example.py] Exception: ', e.data)
                print('[example.py] Exception: ', e.valor)

            print("\nExpression: ", expression)

Extractor()