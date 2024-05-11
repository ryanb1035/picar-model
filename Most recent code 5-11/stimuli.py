from time import sleep
import tkinter
import random

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