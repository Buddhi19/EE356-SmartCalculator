import torch
import numpy as np
import matplotlib.pyplot as plt
from model_load import for_test
from PIL import Image, ImageTk
import cv2


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


class contours:
	def __init__(self,img:np.array):
		self.img = img

	def preprocess(self):
		self.gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
		self.blur = cv2.GaussianBlur(self.gray, (3,3), 0)
		self.bw = cv2.threshold(self.blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

	def plot_img(self):
		plt.imshow(self.img)
		plt.show()

img_test = Image.open("./test_images/test3.png").convert("L")

IMAGE = contours(img_test)
IMAGE.preprocess()
IMAGE.plot_img()

img_test = np.invert(img_test)

plt.imshow(img_test, cmap="gray")
plt.show()

img_proceed = torch.from_numpy(np.array(img_test)).type(torch.FloatTensor)
img_proceed = img_proceed/255.0
img_proceed = img_proceed.unsqueeze(0)
img_proceed = img_proceed.unsqueeze(0)

#display img_proceed
plt.imshow(img_proceed[0][0], cmap="gray")
plt.show()


attention, prediction = for_test(img_proceed)

prediction_text = ""

for i in range(attention.shape[0]):
	if prediction[i] == "<eol>":
		continue
	else:
		prediction_text += prediction[i]

print(prediction_text)