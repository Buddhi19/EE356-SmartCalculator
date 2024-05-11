import numpy as np
import cv2

# Read raw JPEG data from a file
with open('l.jpg', 'rb') as f:
    jpeg_data = f.read()

# Decode the JPEG data
image_np = np.frombuffer(jpeg_data, dtype=np.uint8)
image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

print(jpeg_data)


# Display the image
cv2.imshow('Image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()