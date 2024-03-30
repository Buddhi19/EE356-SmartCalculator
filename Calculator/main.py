import torch
import numpy as np
import matplotlib.pyplot as plt
from model_load import for_test
from PIL import Image, ImageTk
import cv2
import imutils


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

# img_test = Image.open("./test_images/test3.png").convert("L")

img_test = cv2.imread("./test_images/test3.png")

def pre_process(img_test):
	"""
	preprocess the img -> set a black background
	expressions in white
	"""
	img_test = cv2.cvtColor(img_test, cv2.COLOR_BGR2GRAY)
	_, img_test = cv2.threshold(img_test, 85, 255, cv2.THRESH_BINARY)
	img_test = cv2.bitwise_not(img_test)


	plt.imshow(img_test,cmap="gray")
	plt.show()
	return img_test

def model_eligible_format(img_test):
	"""
	make the img_test eligible for the model
	"""
	img_proceed = torch.from_numpy(np.array(img_test)).type(torch.FloatTensor)
	img_proceed = img_proceed/255.0
	img_proceed = img_proceed.unsqueeze(0)
	img_proceed = img_proceed.unsqueeze(0)

	return img_proceed

class Expressions:
	def __init__(self,img):
		self.img = img
		self.expressions = []

	def draw_contours(self):
		"""
		find different expressions or select the expression 
		written area
		"""
		kernel = np.ones((5,5),np.uint8)

		dilation = cv2.dilate(self.img, kernel, iterations = 16) #16

		contours, _ = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

		contours = [cnt for cnt in contours if (cv2.boundingRect(cnt)[2] / cv2.boundingRect(cnt)[3])>=2.0]

		im2 = self.img.copy()
		print(contours)
		for cnt in contours:
			im2 = self.img.copy()
			x, y, w, h = cv2.boundingRect(cnt)
			
			rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (255, 0, 0), 12)
			cropped = im2[y:y + h, x:x + w]
			self.expressions.append(cropped)
		
		return

		
		
	def get_expressions(self):
		for image in self.expressions:
			plt.imshow(image,cmap="gray")
			plt.show()

		return self.expressions


img_test = pre_process(img_test)

EXPRESSIONS = Expressions(img_test)
EXPRESSIONS.draw_contours()
images = EXPRESSIONS.get_expressions()

def predict_expressions(img):
	img_proceed = model_eligible_format(img)

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

for image in images:
	predict_expressions(image)