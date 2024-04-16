import cv2
import numpy as np
from picar import front_wheels, back_wheels
from picamera2 import Picamera2, Preview
import picar
import time

#camera = Picamera2()
#config = camera.create_still_configuration(lores={"size": (3280,2464)}, display="lores")
#camera.start()

picar.setup()
bw = back_wheels.Back_Wheels()
fw = front_wheels.Front_Wheels()
bw.speed = 0

def adjustPosition():
	bw.speed = 30
	cx, cy = find_green_dot()   
	print(cx, cy)
	if abs(cx) < 50:
		bw.speed = 0
		return True
        
	if cx > 0:
		print("turning right")
		fw.turn(90+30)
		t_end = time.time() + 0.5
		while time.time() < t_end:
			bw.backward()
		t_end = time.time() + 0.5
		fw.turn(90)
		while time.time() < t_end:
			bw.forward()
		bw.speed = 0
	else:
		print("turning left")
		fw.turn(90-30)
		t_end = time.time() + 0.5
		while time.time() < t_end:
			bw.backward()
		t_end = time.time() + 0.5
		fw.turn(90)
		while time.time() < t_end:
			bw.forward()
		bw.speed = 0
	return False

def find_green_dot():
	#camera.capture_file("test.png")
	image = cv2.imread("test.png")
	
	hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
	
	lower_green = np.array([30, 40, 40])
	upper_green = np.array([100, 255, 255])
	
	green_mask = cv2.inRange(hsv_image, lower_green, upper_green)
	
	contours,_ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	
	cx = 0
	cy = 0
	
	for contour in contours:
		area = cv2.contourArea(contour)
		if 25 <= area <= 500:
			M = cv2.moments(contour)
			if M["m00"] != 0:
				cx = int(M["m10"] / M["m00"])
				cy = int(M["m01"] / M["m00"])
			
				cv2.drawContours(image, [contour], -1, (0, 255, 0), 2)

	cv2.imwrite('output_with_contours.jpg', image)
	return cx-320, cy-240

#def take_picture():
#	camera.capture_file("test.png")
