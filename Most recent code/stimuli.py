from time import sleep
import tkinter
import os
import random
from PIL import Image, ImageTk

#creating essential variables of the window, the height, and the width of the screen
top = tkinter.Tk()
height = top.winfo_screenheight()
width = top.winfo_screenwidth()
#This version of fullscreen does not include the toolbar
#top.attributes('-fullscreen', True)
#This version of fullscreen does include the toolbar
top.state('zoomed')

#define the canvas
C = tkinter.Canvas(top, bg="white", height=height, width=width)

#Drawing the circle that's supposed to stay constant
right = C.create_oval(width*3/4-100, height/2-100, width*3/4+100, height/2+100, fill='#4b4b4b')

middle = C.create_oval(width/2-20, height/2-20, width/2+20, height/2+20, fill='green2')

#Drawing the circle that's supposed to change
value = random.randint(0,150)
fill = '#%02x%02x%02x' % (value, value, value)
left = C.create_oval(width/4-100, height/2-100, width/4+100, height/2+100, fill=fill) 

#Function to reset the circle and randomly change its size
def display_stimulus():
    C.delete("all")
    middle = C.create_oval(width/2-10, height/2-10, width/2+10, height/2+10, fill='green2')

    #random value between 50 and 400 pixels that represents the radius of the new circle
    value = random.randint(0,150)
    fill = '#%02x%02x%02x' % (value, value, value)
    left = C.create_oval(width/4-100, height/2-100, width/4+100, height/2+100, fill=fill) 
    C.create_text(width/4, height/2, text="{val:.2f}".format(val = (150-value)/150), fill="white", font=("Helvetica 15 bold"))

    #creates a new circle with the generated value
    right = C.create_oval(width*3/4-100, height/2-100, width*3/4+100, height/2+100, fill='#4b4b4b')
    C.create_text(width*3/4, height/2, text="0.50", fill="white", font=("Helvetica 15 bold"))
    C.pack()

# Create the main window
root = tkinter.Toplevel()
root.title("Image Display")

def create_image_canvas():
    # Set the size of the window
    window_width = 800
    window_height = 600
    root.geometry(f"{window_width}x{window_height}")

    # Create a canvas widget
    canvas = tkinter.Canvas(root, width=window_width, height=window_height)
    canvas.pack()

    image_path1 = os.getcwd()+'\\Most recent code\\images\\test1.png'
    image_path2 = os.getcwd()+'\\Most recent code\\images\\test2.png'
    image_path3 = os.getcwd()+'\\Most recent code\\images\\test3.png'

    # Load images
    image1 = Image.open(image_path1)
    image2 = Image.open(image_path2)
    image3 = Image.open(image_path3)

    # Resize images to fit
    image1 = image1.resize((window_width // 2, window_height // 2))
    image2 = image2.resize((window_width // 2, window_height // 2))
    image3 = image3.resize((window_width, window_height // 2))

    # Convert images to PhotoImage format
    tk_image1 = ImageTk.PhotoImage(image1)
    tk_image2 = ImageTk.PhotoImage(image2)
    tk_image3 = ImageTk.PhotoImage(image3)

    # Place images on the canvas
    canvas.create_image(0, 0, anchor="nw", image=tk_image1)
    canvas.create_image(window_width // 2, 0, anchor="nw", image=tk_image2)
    canvas.create_image(0, window_height // 2, anchor="nw", image=tk_image3)


#create_image_canvas()
#display_stimulus()