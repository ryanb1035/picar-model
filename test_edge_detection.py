import cv2
import numpy as np

# Load the image
image_path = 'test.png'
image = cv2.imread(image_path)

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Gaussian blur
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Use Canny edge detection
edges = cv2.Canny(blurred, 50, 150)

# Find contours
contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Function to calculate area of each contour and find the largest one
def find_largest_contour(contours):
    largest_contour = max(contours, key=cv2.contourArea)
    return largest_contour

# Find the largest contour
largest_contour = find_largest_contour(contours)

# Draw the largest contour on the original image
cv2.drawContours(image, [largest_contour], -1, (0, 255, 0), 2)

# Save the resulting image
result_image_path = 'result_test.png'
cv2.imwrite(result_image_path, image)