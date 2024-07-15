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
            
            # Save the block image
            block_image_path = f"{output_dir}/block_{i}.png"
            cv2.imwrite(block_image_path, block_image)
            # print(f"Saved block image: {block_image_path}")

            # Draw the rectangle
            cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)

    # Display the result
    cv2.imshow('Detected Blocks', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return blocks

def is_matrix_present(blocks):
    if not blocks:
        return False

    # Separate blocks into brackets and number
    brackets = [block for block in blocks if block.symbol == '[' or block.symbol == ']']
    numbers = [block for block in blocks if block.symbol != '[' or block.symbol != ']']

    if not brackets or not numbers:
        return False

    # Calculate average size of brackets and numbers
    bracket_areas = [abs((block.bottom_right[1] - block.top_left[1])) for block in brackets]
    number_areas = [abs((block.bottom_right[1] - block.top_left[1])) for block in numbers]

    print(len(bracket_areas))
    print(len(number_areas))

    avg_bracket_area = sum(bracket_areas) / len(bracket_areas)
    avg_number_area = sum(number_areas) / len(number_areas)

    # Compare the average size of brackets to the average size of numbers
    if avg_bracket_area > avg_number_area*2:
        return True
    else:
        return False
    
def output_matrix_in_latex(blocks):
    # Sort blocks by their y-coordinate (top-left corner) to determine rows
    blocks.sort(key=lambda block: block.top_left[1])

    rows = []
    current_row = []
    current_y = blocks[0].top_left[1]

    for block in blocks:
        if abs(block.top_left[1] - current_y) > 20:  # New row if y-coordinate difference is significant
            rows.append(current_row)
            current_row = []
            current_y = block.top_left[1]
        current_row.append(block)
    rows.append(current_row)  # Append the last row

    # Sort each row by the x-coordinate (left to right)
    for row in rows:
        row.sort(key=lambda block: block.top_left[0])

    # Generate LaTeX code for the matrix
    latex_matrix = "\\begin{bmatrix}\n"
    for row in rows:
        row_symbols = " & ".join([block.symbol for block in row])
        latex_matrix += row_symbols + " \\\\\n"
    latex_matrix += "\\end{bmatrix}"

    return latex_matrix


if __name__ == "__main__":
    # Path to the image
    image_path = 'images/image.png'
    output_dir = 'images/blocks'
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Detect blocks and save them as separate images
    blocks = detect_blocks_using_connected_components(image_path, output_dir)

    blocks[0].symbol = "["
    blocks[1].symbol = "]"
    blocks[2].symbol = "1"
    blocks[3].symbol = "4"
    blocks[4].symbol = "-13"
    blocks[5].symbol = "20"
    blocks[6].symbol = "5"
    blocks[7].symbol = "-6"


    is_mat = is_matrix_present(blocks)
    print(is_mat)
    print(output_matrix_in_latex(blocks))

    # Print the details of each block
    # for block in blocks:
    #     print(block)