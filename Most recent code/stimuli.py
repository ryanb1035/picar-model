from time import sleep
import tkinter
import os
import random
from PIL import Image, ImageTk

# These are the darkness values for both the left and right circles
# Since the left circle is variable it's set at 0 to begin with
# Since the right circle is constant it's set to 0.5 and doesn't change 
left_circle = 0
right_circle = 0.5

#creating essential variables of the window, the height, and the width of the stimulus screen
stimulus = tkinter.Tk()
height = stimulus.winfo_screenheight()
width = stimulus.winfo_screenwidth()
stimulus.state('zoomed')

# Create the main window
visualization = tkinter.Toplevel()
visualization.title("Image Display")

#define the canvas
canvas_s = tkinter.Canvas(stimulus, bg="white", height=height, width=width)

# Drawing the circle that's supposed to stay constant
right = canvas_s.create_oval(width*3/4-100, height/2-100, width*3/4+100, height/2+100, fill='#4b4b4b')

# Drawing the circle in the middle colored bright green meant for the robot to use for centering
middle = canvas_s.create_oval(width/2-20, height/2-20, width/2+20, height/2+20, fill='green2')

# Drawing the circle that's supposed to change transparency
# Value is a random number from 1 to 150 representing how dark the circle will be
value = random.randint(0,150)
# Using this value, a HEX value is generated for the color
fill = '#%02x%02x%02x' % (value, value, value)
# The left circle is filled with this color
left = canvas_s.create_oval(width/4-100, height/2-100, width/4+100, height/2+100, fill=fill) 

#Function to reset the circle and randomly change its color
def display_stimulus():
    # THis method clears the entire canvas so everything can be redrawn
    canvas_s.delete("all")

    # First, the middle circle is regenerated
    middle = canvas_s.create_oval(width/2-10, height/2-10, width/2+10, height/2+10, fill='green2')

    # Similar to the process above, a value between 1 and 150 is chosen and its HEX value is what fills the circle
    value = random.randint(0,150)
    fill = '#%02x%02x%02x' % (value, value, value)
    left = canvas_s.create_oval(width/4-100, height/2-100, width/4+100, height/2+100, fill=fill) 

    # The global variable defining the left circle's darkness at any given time is changed
    # The values for this variable range from 0 to 1 since it's divided by the maximum value of 150
    left_circle = (150-value)/150

    # The darkness value of this circle is outputted on the model for easy visualization
    canvas_s.create_text(width/4, height/2, text="{val:.2f}".format(val = left_circle, fill="white", font=("Helvetica 15 bold")))

    # Right circle is generated with the same fill color as before
    right = canvas_s.create_oval(width*3/4-100, height/2-100, width*3/4+100, height/2+100, fill='#4b4b4b')

    # The darkness value of this circle is outputted on the model for easy visualization
    canvas_s.create_text(width*3/4, height/2, text="0.50", fill="white", font=("Helvetica 15 bold"))

    # The canvas is packed
    canvas_s.pack()

# Create a canvas widget for the plots and pictures
canvas_v = tkinter.Canvas(visualization, bg="white", height=height, width=width)

# Define the paths of each image, done using os so it works on any computer running this program
image_path1 = os.getcwd()+'\\Most recent code\\images\\test1.png'
image_path2 = os.getcwd()+'\\Most recent code\\images\\test2.png'
image_path3 = os.getcwd()+'\\Most recent code\\images\\test3.png'

# method to make another GUI window, this time showing plots and pictures
def create_image_canvas():
    # Load images
    image1 = Image.open(image_path1)
    image2 = Image.open(image_path2)
    image3 = Image.open(image_path3)

    # Resize images to fit into the box, where two will be on the top half of the screen and the other will be on the bottom
    image1 = image1.resize((width // 2, height // 2))
    image2 = image2.resize((width // 2, height // 2))
    image3 = image3.resize((width, height // 2))

    # Convert images to PhotoImage format
    tk_image1 = ImageTk.PhotoImage(image1)
    tk_image2 = ImageTk.PhotoImage(image2)
    tk_image3 = ImageTk.PhotoImage(image3)

    # Place images on the canvas
    canvas_v.create_image(0, 0, image=tk_image1)
    canvas_v.create_image(width // 2, 0, image=tk_image2)
    canvas_v.create_image(0, height // 2, image=tk_image3)

    # The canvas is packed
    canvas_v.pack()