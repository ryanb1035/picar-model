import cv2
import numpy as np
from picar import front_wheels, back_wheels # type: ignore
from picamera2 import Picamera2, Preview # type: ignore
import picar # type: ignore
import time
from time import sleep
import new_screen_centering

camera = Picamera2()
config = camera.create_still_configuration(main={"size": (3280,2464)}, lores={"size": (640,480)}, encode="lores")
camera.start()

camera.capture_file("test.png")
image = cv2.imread("test.png")[820:2460, 616:1848]

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (7,7), 0)

edges = cv2.Canny(blurred, 50, 150)

contours,_ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours = sorted(contours, key=cv2.contourArea)

def is_circle(contour):
	area = cv2.contourArea(contour)
	if area < 300:
		print("area")
		return False
	perimiter = cv2.arcLength(contour, True)
	if perimiter == 0:
		return False
	circularity = 4 * np.pi * (area / (perimiter * perimiter))
	if circularity < 0.8:
		print("circularity")
		return False
	(x,y), (width, height), angle = cv2.minAreaRect(contour)
	aspect_ratio = min(width, height) / max(width, height)
	if aspect_ratio < 0.85:
		print("ratio")
		return False
	print("passed")
	return True

stimuli = []
for i in contours:
	if is_circle(i):
		stimuli.append(i)
		cv2.drawContours(image, i, -1, (0, 255, 0), 2)

print(len(stimuli))

#cv2.imwrite("result.png", image)

if len(stimuli) == 2:
	x1,y1,w1,h1 = cv2.boundingRect(stimuli[0])
	#print("first", cv2.boundingRect(stimuli[0]))
	x2,y2,w2,h2 = cv2.boundingRect(stimuli[1])
	#print("second", cv2.boundingRect(stimuli[1]))
	mask1 = np.zeros_like(image[:2])
	mask2 = np.zeros_like(image[:2])

    # Draw the contours on the masks
	cv2.drawContours(mask1, [stimuli[0]], -1, color=255, thickness=cv2.FILLED)
	cv2.drawContours(mask2, [stimuli[1]], -1, color=255, thickness=cv2.FILLED)

    # Calculate the mean intensity within each mask
	mean_intensity1 = cv2.mean(image, mask=mask1)[0]
	mean_intensity2 = cv2.mean(image, mask=mask2)[0]

	if x1 < x2:
		stimulus_1 = mean_intensity1
		stimulus_2 = mean_intensity2
	else:
		stimulus_1 = mean_intensity2
		stimulus_2 = mean_intensity1
	temp = stimulus_1 + stimulus_2
	stimulus_1 = stimulus_1/temp
	stimulus_2 = stimulus_2/temp
else:
	stimulus_1 = 10
	stimulus_2 = 9
	
print(stimulus_1, stimulus_2)

cv2.imwrite("result.png", image)

# model implementation
# Setting constants for the attentional model.
# constants
r_out = 0.01
r_in = 0.8

m = 5
h = 30
s50 = 8
k = 7

d_out = 0.05
d_in = 1

a = 5.3
b = 22.2
L50 = 11.6

# determining baseline inhibitory activity (i.e. inhibitory unit activity at t0)
inhibition_tminus1 = m
predifference = 1

# Implementing a loop to simulate dynamic inhibitory activity over time.
while predifference > 0.05:
    # dependent on inhibition_tminus1_2
    i_in = r_in * inhibition_tminus1
    i_out = r_out * inhibition_tminus1
   
    # inhibitory unit activity at current time step
    inhibition_t0 = (1 / (i_out + 1)) * ((m / (i_in + 1)))
   
    # computing % change in inhibitory neuron activity from previous time step
    predifference = abs(1 - (inhibition_t0 / inhibition_tminus1))
   
    # updating inhibitory unit activity
    inhibition_tminus1 = inhibition_t0
   
# print('baseline inhibitory activity: {0}'.format(inhibition_t0))

inhibition_t0_1 = inhibition_t0
inhibition_t0_2 = inhibition_t0

# stimulus strengths
# Processing the strength of stimuli based on the detected objects.
stimulus_strength = []
"""
# leftmost stimulus
temp = min(stimulus_strength_dict)
stimulus_strength.append(stimulus_strength_dict[temp])
# rightmost stimulus
temp = max(stimulus_strength_dict)
stimulus_strength.append(stimulus_strength_dict[temp])


stimulus_strength[1] = stimulus_strength[1]/1200
stimulus_strength[0] = stimulus_strength[0]/1200

# stimulus 1 is always the stimulus on the left
stimulus_1 = stimulus_strength[0]
stimulus_2 = stimulus_strength[1]
"""




"""
for testing purposes
"""
"""
stimulus_1 = 9
stimulus_2 = 10
"""

print('stimulus strength 1: {0}'.format(stimulus_1))
print('stimulus strength 2: {0}'.format(stimulus_2))

fano_factor = 0.25

# Simulating the effect of each stimulus on the attentional model.
for k in range(101):
    # dependent on inhibition_t0_2
    i_in_1 = r_in * inhibition_t0_2
    i_out_1 = r_out * inhibition_t0_2
   
    # dependent on inhibition_t0_1
    i_in_2 = r_in * inhibition_t0_1
    i_out_2 = r_out * inhibition_t0_1
   
    # inhibitory unit activity at current time step
    inhibition_t1_1 = (1 / (i_out_1 + 1)) * ((m / (i_in_1 + 1)) + h * ((stimulus_1 ** k) / ((stimulus_1 ** k) + (s50 ** k) + (i_in_1 ** k))))
    inhibition_t1_2 = (1 / (i_out_2 + 1)) * ((m / (i_in_2 + 1)) + h * ((stimulus_2 ** k) / ((stimulus_2 ** k) + (s50 ** k) + (i_in_2 ** k))))
   
    # dependent on inhibition_t1_2
    s_in_1 = d_in * (inhibition_t1_2 + inhibition_t1_1)
    s_out_1 = d_out * (inhibition_t1_2 + inhibition_t1_1)
   
    # dependent on inhibition_t1_1
    s_in_2 = d_in * (inhibition_t1_1 + inhibition_t1_2)
    s_out_2 = d_out * (inhibition_t1_1 + inhibition_t1_2)
   
    # OT neuron activity at current time step
    OT_t1_1 = (1 / (s_out_1 + 1)) * ((a / (s_in_1 + 1)) + b * (np.square(stimulus_1) / (np.square(stimulus_1) + np.square(L50) + np.square(s_in_1))))
    OT_t1_2 = (1 / (s_out_2 + 1)) * ((a / (s_in_2 + 1)) + b * (np.square(stimulus_2) / (np.square(stimulus_2) + np.square(L50) + np.square(s_in_2))))
    
    # adding noise 
    OT_t1_1 = OT_t1_1 + (np.sqrt(OT_t1_1 * fano_factor) * np.random.normal())
    OT_t1_2 = OT_t1_2 + (np.sqrt(OT_t1_2 * fano_factor) * np.random.normal())
    
    # updating inhibitory unit activity
    inhibition_t0_1 = inhibition_t1_1
    inhibition_t0_2 = inhibition_t1_2
   
   
print('final excitatory unit 1 activity: {0}'.format(OT_t1_1))
print('final excitatory unit 2 activity: {0}'.format(OT_t1_2))

# Setting up the PiCar for movement.
# moving the robot towards the winning stimulus
picar.setup()
bw = back_wheels.Back_Wheels()
fw = front_wheels.Front_Wheels()
bw.speed = 0
# Determining the direction of movement based on the dominant stimulus.
# Moving the car towards the stronger stimulus.
if OT_t1_1 > OT_t1_2: # stimulus on the left is bigger
	print("left stimulus")
	print(OT_t1_1, OT_t1_2)
	fw.turn(90-30)
	bw.speed = 30
	t_end = time.time() + 1
	while time.time() < t_end:
		bw.backward()
	bw.speed = 0
	fw.turn(90)
	bw.speed = 30
	t_end = time.time() + 1
	while time.time() < t_end:
		bw.forward()
	bw.speed = 0
    
   
else: # stimulus on the right is bigger
	print("right stimulus")
	print(OT_t1_1, OT_t1_2)
	fw.turn(90+30)
	bw.speed = 30
	t_end = time.time() + 1
	while time.time() < t_end:
		bw.backward()
	bw.speed = 0
	fw.turn(90)
	bw.speed = 30
	t_end = time.time() + 1
	while time.time() < t_end:
		bw.forward()
	bw.speed = 0

sleep(1)

while new_screen_centering.adjustPosition() != True:
	camera.capture_file("test.png")