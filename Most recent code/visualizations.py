import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os

print(os.getcwd())

# Paths to your images
image_path1 = os.getcwd()+'\\Most recent code\\images\\test1.png'
image_path2 = os.getcwd()+'\\Most recent code\\images\\test2.png'
image_path3 = os.getcwd()+'\\Most recent code\\images\\test3.png'

# Load the images
img1 = mpimg.imread(image_path1)
img2 = mpimg.imread(image_path2)
img3 = mpimg.imread(image_path3)

# Create a figure to hold the subplots
fig1 = plt.figure()

# Add subplots
# Two images on the top
ax1 = fig1.add_subplot(2, 2, 1)  # Row 1, Col 1
ax2 = fig1.add_subplot(2, 2, 2)  # Row 1, Col 2
# One image on the bottom spanning both columns
ax3 = fig1.add_subplot(2, 1, 2)  # Row 2, Col span

# Display images
ax1.imshow(img1)
ax1.axis('off')  # Turn off axis
ax2.imshow(img2)
ax2.axis('off')
ax3.imshow(img3)
ax3.axis('off')

# Adjust layout
plt.tight_layout()

# Show the plot
plt.show()
