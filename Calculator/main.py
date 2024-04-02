import torch
import numpy as np
import matplotlib.pyplot as plt
from model_load import for_test
from PIL import Image, ImageTk
import cv2
import imutils


def pre_process(img_test):
	"""
	preprocess the img -> set a black background
	expressions in white
	"""
	img_test = cv2.cvtColor(img_test, cv2.COLOR_BGR2GRAY)
	_, img_test = cv2.threshold(img_test, 150, 255, cv2.THRESH_BINARY) # 85 # 155
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
		kernel = np.ones((10,4),np.uint8)  #10,10

		dilation = cv2.dilate(self.img, kernel, iterations = 16) #16

		# dilation = cv2.morphologyEx(self.img, cv2.MORPH_OPEN, kernel)

		contours, _ = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

		contours = [cnt for cnt in contours if (cv2.boundingRect(cnt)[2] / cv2.boundingRect(cnt)[3])>=1.0]

		im2 = self.img.copy()
		print(contours)
		for cnt in contours:
			im2 = self.img.copy()
			x, y, w, h = cv2.boundingRect(cnt)
			
			rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (255, 0, 0), 0)
			cropped = im2[y:y + h, x:x + w]
			self.expressions.append(cropped)
		
		return
	
	def get_expressions(self):
		"""
		Get all expression containing images
		"""
		for image in self.expressions:
			plt.imshow(image,cmap="gray")
			plt.show()

		return self.expressions

def predict_expressions(img):
	"""
	predicting expressions
	"""
	img_proceed = model_eligible_format(img)

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


def run_for_std_scenario():
	img_test = cv2.imread("./test_images/test10.png")
	img_test = pre_process(img_test)

	EXPRESSIONS = Expressions(img_test)
	EXPRESSIONS.draw_contours()
	images = EXPRESSIONS.get_expressions()

	for image in images:
		cv2.imwrite("./results/result_1.bmp",image)
		image = Image.open("./results/result_1.bmp").convert("L")
		predict_expressions(image)

def run_for_training_scenario():
	img_test = Image.open("./results/result_1.png").convert("L")
	predict_expressions(img_test)

# run_for_training_scenario()
run_for_std_scenario()



