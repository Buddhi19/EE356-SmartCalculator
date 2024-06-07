# Author : Athulya Ratnayake
# File : matrix_detection.py
# Date : 2024/05/05

# Import modules
import cv2 as cv
import matplotlib.pyplot as plt

# Define path to the image
img_path = "images/Matrix_hr2.jpg"

#Read image
img = cv.imread(img_path)

# Convert into grayscale
gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

# Show image
# cv.imshow('image', image)
# cv.waitKey(0)

# Convert to a binary image
retval, binary_img = cv.threshold(gray_img, 127, 255, cv.THRESH_BINARY)

# Show binary image
# cv.imshow('Binary Image', binary_img)
# cv.waitKey(0)

# Canny edge detection
edges = cv.Canny(binary_img, 100, 200)

# Plotting results
plt.subplot(121),plt.imshow(binary_img,cmap = 'gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(edges,cmap = 'gray')
plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
 
plt.show()