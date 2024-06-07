import cv2
import numpy as np

def detect_blocks_using_connected_components(image_path):
    # Load the image
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV)

    # Perform connected components analysis
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(binary, connectivity=8)

    # Filter and draw rectangles around the blocks
    for i in range(1, num_labels):  # Skip the background label
        x, y, w, h, area = stats[i]
        if area > 50:  # Filter small components
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Display the result
    cv2.imshow('Detected Blocks', image)
    cv2.waitKey(0)
    # cv2.destroyAllWindows()

if __name__ == "__main__":
    # Path to the image
    image_path = 'images/Matrix_hr2.jpg'
    detect_blocks_using_connected_components(image_path)
    
