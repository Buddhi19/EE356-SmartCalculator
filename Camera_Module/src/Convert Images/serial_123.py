import cv2
import numpy as np
f = open("image.txt", "r")

image_data = f.read()

image_data = image_data.split(" ")

#convert image data to numpy array

image_data = np.array(image_data, dtype=np.uint8)

#use pillow to display image
from PIL import Image
img = Image.fromarray(image_data)


img.show()