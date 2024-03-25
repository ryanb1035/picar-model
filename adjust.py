from picar import front_wheels, back_wheels
import picar
from PIL import Image
import numpy as np
import cv2
import io
from picamera import PiCamera

h = 640 #largest resolution length
cam_res = (int(h),int(0.75*h)) # resizing to picamera's required ratios
cam_res = (int(32*np.floor(cam_res[0]/32)),int(16*np.floor(cam_res[1]/16)))

cam = PiCamera(resolution=cam_res)

data = np.empty((cam_res[1],cam_res[0],3),dtype=np.uint8)
data = data[100:300, 100:500, 0:3]

# Load the image using OpenCV
image = cv2.imread(data)

# Convert the image to grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply a threshold to isolate the white screen
# Assuming that the white screen has a pixel value close to 255
# We pick a threshold value (e.g., 200) to differentiate the screen from the rest of the image
_, thresholded_image = cv2.threshold(gray_image, 200, 255, cv2.THRESH_BINARY)

# Find contours from the thresholded image
contours, _ = cv2.findContours(thresholded_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Find the largest contour which should be the screen
largest_contour = max(contours, key=cv2.contourArea)

# Calculate the area of the largest contour
screen_area = cv2.contourArea(largest_contour)

# Calculate the total area of the image
total_area = image.shape[0] * image.shape[1]

# Calculate the percentage of the screen relative to the total image
screen_percentage = (screen_area / total_area) * 100

# Find the centroid (center) of the screen contour
M = cv2.moments(largest_contour)
cx = int(M['m10']/M['m00'])
cy = int(M['m01']/M['m00'])

# Determine the position of the centroid relative to the image center
image_center_x = image.shape[1] // 2

# The screen is to the right if the centroid x-coordinate is greater than the image center x-coordinate
position = "right" if cx > image_center_x else "left"

picar.setup()
bw = back_wheels.Back_Wheels()
fw = front_wheels.Front_Wheels()
bw.speed = 0

if position == "right":
    fw.turn(90+(math.abs(cx-image_center_x)))
    bw.speed = 30
    for i in range(500):
        bw.backward()
    bw.stop()
    fw.turn(90)
else:
    fw.turn(90-(math.abs(cx-image_center_x)))
    bw.speed = 30
    for i in range(500):
        bw.backward()
    bw.stop()
    fw.turn(90)