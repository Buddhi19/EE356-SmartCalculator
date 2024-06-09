import cv2
import numpy as np
import os

class SymbolBlock:
    def __init__(self, image, top_left, bottom_right):
        self.image = image
        self.top_left = top_left
        self.bottom_right = bottom_right
        self.symbol = None

    def __str__(self):
        return f"Symbol: {self.symbol}, Top-left: {self.top_left}, Bottom-right: {self.bottom_right}"

def detect_blocks_using_connected_components(image_path, output_dir):
    # Load the image
    image_ori = cv2.imread(image_path)
    image = cv2.resize(image_ori, (582,283))
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply adaptive thresholding
    _, binary_not = cv2.threshold(gray, 110, 255, cv2.THRESH_BINARY)

    binary = cv2.bitwise_not(binary_not)

    # Use morphological operations to enhance the image
    kernel = np.ones((30, 30), np.uint8)
    dilated = cv2.dilate(binary, kernel, iterations=1)
    eroded = cv2.erode(dilated, kernel, iterations=1)

    # Perform connected components analysis
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(eroded, connectivity=8)

    # Create a list to store SymbolBlock objects
    blocks = []

    # Filter and draw rectangles around the blocks, and save each block as an image
    for i in range(1, num_labels):  # Skip the background label
        x, y, w, h, area = stats[i]
        if area > 50:  # Filter small components
            top_left = (x, y)
            bottom_right = (x + w, y + h)
            
            # Ensure correct assignment of top-left and bottom-right corners
            assert top_left[0] <= bottom_right[0], "Top-left x-coordinate should be less than or equal to bottom-right x-coordinate"
            assert top_left[1] <= bottom_right[1], "Top-left y-coordinate should be less than or equal to bottom-right y-coordinate"

            block_image = image[y:y+h, x:x+w]
            
            # Create a SymbolBlock object and add it to the list
            block = SymbolBlock(block_image, top_left, bottom_right)
            blocks.append(block)
            
            # Save the block image (optional)
            block_image_path = f"{output_dir}/block_{i}.png"
            cv2.imwrite(block_image_path, block_image)
            print(f"Saved block image: {block_image_path}")

            # Draw the rectangle (optional)
            cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)

    # Display the result (optional)
    cv2.imshow('Detected Blocks', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return blocks

# Path to the image
image_path = 'images/image.png'
output_dir = 'images/blocks'  # Specify the directory to save block images

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Detect blocks and save them as separate images
blocks = detect_blocks_using_connected_components(image_path, output_dir)

# Print the details of each block
for block in blocks:
    print(block)