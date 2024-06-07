import cv2
import numpy as np
from matplotlib import pyplot as plt

def enhance_and_detect_edges(image_path):
    # Load the image
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        print(f"Error: Unable to open image at {image_path}")
        return

    # Apply adaptive thresholding to convert to binary image
    adaptive_thresh = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                            cv2.THRESH_BINARY_INV, 11, 2)

    # Perform dilation to enhance the features
    kernel = np.ones((3, 3), np.uint8)
    dilated = cv2.dilate(adaptive_thresh, kernel, iterations=1)

    # Detect edges using Canny edge detection with adjusted parameters
    edges = cv2.Canny(dilated, 50, 150, apertureSize=3)

    # Display the images
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 3, 1), plt.title('Original Image'), plt.imshow(image, cmap='gray'), plt.axis('off')
    plt.subplot(1, 3, 2), plt.title('Dilated Image'), plt.imshow(dilated, cmap='gray'), plt.axis('off')
    plt.subplot(1, 3, 3), plt.title('Edge Image'), plt.imshow(edges, cmap='gray'), plt.axis('off')
    plt.show()

# Path to the uploaded image
image_path = 'images/Matrix_hr.jpg'

# Enhance and detect edges
enhance_and_detect_edges(image_path)
