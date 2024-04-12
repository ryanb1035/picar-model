import cv2
import numpy as np
import screen_cropper

"""
#Contouring all the object on screen
"""

# Load the image
image = cv2.imread(screen_cropper.cropped_image_path)
#image = cv2.imread("test.png")

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Gaussian blur
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Use Canny edge detection
edges = cv2.Canny(blurred, 50, 150)

# Find contours
contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#make a list of circular contours
contour_list = []
for contour in contours:
    approx = cv2.approxPolyDP(contour,0.01*cv2.arcLength(contour,True),True)
    area = cv2.contourArea(contour)
    if ((len(approx) > 10) & (area > 1000) & (area < 100000)):
        contour_list.append(contour)

# Draw the largest contour on the original image
for i in contour_list:
    cv2.drawContours(image, i, -1, (0, 255, 0), 2)

# Save the resulting image
result_image_path = 'result_test.png'
cv2.imwrite(result_image_path, image)