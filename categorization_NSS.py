import time
from picamera import PiCamera
import scipy.ndimage as scimg
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle
from sklearn.cluster import DBSCAN

from picar import front_wheels, back_wheels
import picar


# Setting up the PiCamera with specific resolution settings.
# 'h' is the length of the resolution, and the resolution is adjusted
# to meet PiCamera's aspect ratio requirements.
# An empty data array is preallocated for storing the captured images.
h = 640 #largest resolution length
cam_res = (int(h),int(0.75*h)) # resizing to picamera's required ratios
cam_res = (int(32*np.floor(cam_res[0]/32)),int(16*np.floor(cam_res[1]/16)))
cam = PiCamera(resolution=cam_res)
# Capturing an image from the PiCamera and storing it in the 'data' array.
# preallocating image variables
data = np.empty((cam_res[1],cam_res[0],3),dtype=np.uint8)

# different edge detection methods
fig,ax = plt.subplots(2,1,figsize=(10,6))
t1 = time.time()
cam.capture(data,'rgb') # capture image

"""
TODO: crop data appropriately
"""
data = data[100:300, 100:500, 0:3]

fig2,ax2 = plt.subplots(1,1,figsize=(12,8))
ax2.imshow(data)
 
# Applying a Gaussian filter to the image for edge detection, and creating a grid for the image data.
scale_val = 0.25
min_samps = 20
leaf_sz = 15
max_dxdy = 35
gaus = scimg.fourier_gaussian(scimg.zoom(np.mean(data,2),scale_val),sigma=0.01)
x,y = np.meshgrid(np.arange(0,np.shape(data)[1],1/scale_val),
                  np.arange(0,np.shape(data)[0],1/scale_val))

# The Canny edge detection method is used without angle to detect edges.
# A histogram of edge intensities is created to identify significant edges. 
can_x = scimg.prewitt(gaus,axis=0)
can_y = scimg.prewitt(gaus,axis=1)
can = np.hypot(can_x,can_y)
ax[0].pcolormesh(x,y,gaus)
# pulling out object edges
bin_size = 100 # total bins to show
percent_cutoff = 0.018 # cutoff once main peak tapers to 1% of max
hist_vec = np.histogram(can.ravel(),bins=bin_size)
hist_x,hist_y = hist_vec[0],hist_vec[1]
for ii in range(np.argmax(hist_x),bin_size):
    hist_max = hist_y[ii]
    if hist_x[ii]<percent_cutoff*np.max(hist_x):
        break

# sklearn section for clustering
x_cluster = x[can>hist_max]
y_cluster = y[can>hist_max]
x_scaled = np.where(can>hist_max,x,0)
y_scaled = np.where(can>hist_max,y,0)
scat_pts = []
for ii,jj in zip(x_cluster,y_cluster):
    scat_pts.append((ii,jj))
   
# clustering analysis for object detection
# Using DBSCAN clustering algorithm to identify clusters of edge points.
# These clusters help in detecting distinct objects in the image.
clustering = DBSCAN(eps=max_dxdy,min_samples=min_samps,
                    algorithm='ball_tree',
                    leaf_size=leaf_sz).fit(scat_pts)
nn_time = time.time()-t1

stimulus_strength_dict = {}

# looping through each individual object
# Analyzing each detected object. Objects too close to the image edge are ignored.
for ii in np.unique(clustering.labels_):    
    if ii==-1:
        continue
    clus_dat = np.where(clustering.labels_==ii)

    x_pts = x_cluster[clus_dat]
    y_pts = y_cluster[clus_dat]
    cent_mass = (np.mean(x_pts),np.mean(y_pts))
    if cent_mass[0]<np.min(x)+10 or cent_mass[0]>np.max(x)-10 or\
       cent_mass[1]<np.min(y)+10 or cent_mass[1]>np.max(y)-10:
        continue
   
    ax[1].plot(x_pts,y_pts,marker='.',linestyle='',
               label='Unrotated Scatter')
    # rotation algorithm
    # Rotating the coordinate system for better object representation.
    evals,evecs = np.linalg.eigh(np.cov(x_pts,y_pts))
    angle = np.arctan(evecs[0][1]/evecs[0][0])
    # print(str((angle/np.pi)*180))
    rot_vec = np.matmul(evecs.T,[x_pts,y_pts])
   
    # rectangle algorithms
    # Calculating bounding rectangles for each object and annotating them on the image.
    if angle<0:
        rect_origin = (np.matmul(evecs,[np.min(rot_vec[0]),np.max(rot_vec[1])]))
    else:
        rect_origin = (np.matmul(evecs,[np.max(rot_vec[0]),np.min(rot_vec[1])]))
       
    rect_width = np.max(rot_vec[0])-np.min(rot_vec[0])
    rect_height = np.max(rot_vec[1])-np.min(rot_vec[1])
    obj_rect = Rectangle(rect_origin,rect_width,rect_height,angle=(angle/np.pi)*180)
    pc = PatchCollection([obj_rect], facecolor = "None", edgecolor='r',linewidth=2)
    ax2.add_collection(pc)
    ax2.annotate('{0:2.0f}$^\circ$ Rotation'.format((angle/np.pi)*180),
                 xy=(rect_origin),
                 xytext=(0,0),textcoords='offset points',
                 bbox=dict(fc='white'))
   
    # stuff i added
    # Calculating object's area and storing it with its x-coordinate in a dictionary.
    radius = (rect_width + rect_height) / 4
    area = np.pi * np.square(radius)
    stimulus_strength_dict[int(rect_origin[0])] = area # key = x coordinate, value = area 
   
   
ax[1].set_xlim(np.min(x),np.max(x))
ax[1].set_ylim(np.min(y),np.max(y))

# print('total time: {0:2.1f}'.format(time.time()-t1))
fig2.savefig('rectangles_over_real_image.png',dpi=200,facecolor=[252/255,252/255,252/255])
# plt.show()


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

"""
TODO: scale stimulus accordingly
"""
stimulus_strength[1] = stimulus_strength[1]/1200
stimulus_strength[0] = stimulus_strength[0]/1200

# stimulus 1 is always the stimulus on the left
stimulus_1 = stimulus_strength[0]
stimulus_2 = stimulus_strength[1]

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
    fw.turn(90 - 30)
    bw.speed = 30
    for i in range(500):
        bw.backward()
    bw.stop()
    fw.turn(90)
   
else: # stimulus on the right is bigger
    fw.turn(90 + 30)
    bw.speed = 30
    for i in range(500):
        bw.backward()
    bw.stop()
    fw.turn(90)
