import screen_cropper
import cv2
import numpy as np

"""
#Contouring all the object on screen
"""

# Load the image
image = cv2.imread(screen_cropper.cropped_image_path)

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Gaussian blur
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Use Canny edge detection
edges = cv2.Canny(blurred, 50, 150)

# Find contours
contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Find the largest contour
largest_contour = max(contours, key=cv2.contourArea)

# Draw the largest contour on the original image
cv2.drawContours(image, contours[0:3], -1, (0, 255, 0), 2)

# Save the resulting image
result_image_path = 'result_test.png'
cv2.imwrite(result_image_path, image)





"""
# Inputting contours into neural circuit
"""
"""
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

# leftmost stimulus
temp = min(stimulus_strength_dict)
stimulus_strength.append(stimulus_strength_dict[temp])
# rightmost stimulus
temp = max(stimulus_strength_dict)
stimulus_strength.append(stimulus_strength_dict[temp])


TODO: scale stimulus accordingly

stimulus_strength[1] = stimulus_strength[1]/1200
stimulus_strength[0] = stimulus_strength[0]/1200

# stimulus 1 is always the stimulus on the left
stimulus_1 = stimulus_strength[0]
stimulus_2 = stimulus_strength[1]


for testing purposes

stimulus_1 = 9
stimulus_2 = 10


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
"""