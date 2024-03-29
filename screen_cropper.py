import cv2
import numpy as np
from scipy import ndimage

# Function to find the largest rectangle contour in the image
def find_laptop_screen_contour(contours):
    laptop_contour = max(contours, key=cv2.contourArea)
    return laptop_contour

# Load the image
image = cv2.imread("test.png")

# Convert to grayscale and apply Gaussian blur
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (7, 7), 0)

# Detect edges
edges = cv2.Canny(blurred, 50, 150)

# Find contours
contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Find the laptop screen contour
laptop_screen_contour = find_laptop_screen_contour(contours)

# Get the bounding rectangle for the laptop screen contour
x, y, w, h = cv2.boundingRect(laptop_screen_contour)

# Crop the image to the bounding rectangle
cropped_image = image[y:y+h, x:x+w]

# Save the cropped image
cropped_image_path = 'cropped_laptop_screen.png'
cv2.imwrite(cropped_image_path, cropped_image)

# Calculate the angle of rotation and the rectangle's position relative to the center of the screen
# We assume the contour of the laptop screen is approximately a rectangle.
rect = cv2.minAreaRect(laptop_screen_contour)
box = cv2.boxPoints(rect)
box = np.intp(box)

# Calculate the center of the image
image_center = (image.shape[1]//2, image.shape[0]//2)

# Calculate the center of the rectangle
rect_center = (int(rect[0][0]), int(rect[0][1]))

# Calculate the angle of rotation
angle_of_rotation = rect[2]

# The position of the rectangle relative to the image center
position_relative_to_center = (rect_center[0] - image_center[0], rect_center[1] - image_center[1])

# Annotate the original image with the bounding box
annotated_image = image.copy()
cv2.drawContours(annotated_image, [box], 0, (0, 255, 0), 2)

# Save the annotated image with bounding box
annotated_image_path = 'annotated_laptop_screen.png'
cv2.imwrite(annotated_image_path, annotated_image)

cropped_image_path, annotated_image_path, angle_of_rotation, position_relative_to_center
