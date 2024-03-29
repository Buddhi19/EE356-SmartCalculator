import torch
import numpy as np
import matplotlib.pyplot as plt
from model_load import for_test
from PIL import Image, ImageTk


def imresize(im,sz):
    pil_im = Image.fromarray(im)
    return np.array(pil_im.resize(sz))

def resize( w_box, h_box, pil_image): 
	w, h = pil_image.size 
	f1 = 1.0*w_box/w 
	f2 = 1.0*h_box/h    
	factor = min([f1, f2])   
	width = int(w*factor)    
	height = int(h*factor)    
	return pil_image.resize((width, height), Image.ANTIALIAS)  

img_test = Image.open("./test_images/test1.png").convert("L")

