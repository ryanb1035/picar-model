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
right = C.create_oval(width*3/4-100, height/2-100, width*3/4+100, height/2+100, fill='black')

middle = C.create_oval(width/2-10, height/2-10, width/2+10, height/2+10, fill='green2')

#Drawing lines for the robot to reorient itself
#horizontal = C.create_line(0, height/2, width, height/2)
#vertical = C.create_line(width/2, 0, width/2, height)

#Drawing the circle that's supposed to change
value = random.randint(25,175)
left = C.create_oval(width/4-value, height/2-value, width/4+value, height/2+value, fill="black") 

#Function to reset the circle and randomly change its size
def display_stimulus():
    #Simplest method I could figure out to "erase" the screen on the left side
    #Draws a white rectangle over everything and redraws the horizontal line
    left = C.create_rectangle(0, 0, width, height, fill="white")
    middle = C.create_oval(width/2-10, height/2-10, width/2+10, height/2+10, fill='green2')

    #horizontal = C.create_line(0, height/2, width, height/2)

    #random value between 50 and 400 pixels that represents the radius of the new circle
    value = random.randint(25,175)

    #creates a new circle with the generated value
    right = C.create_oval(width*3/4-100, height/2-100, width*3/4+100, height/2+100, fill='black')
    left = C.create_oval(width/4-value, height/2-value, width/4+value, height/2+value, fill="black") 

    C.pack()

    print("The radius of the new circle is",value,"pixels")

#Programming the button to call the above function every time it's pressed
B = tkinter.Button(top, text ="reset", command=display_stimulus)
B.place(x=0,y=0)

B.pack()
display_stimulus()
top.mainloop()

#display_stimulus()
#C.pack()
#top.mainloop()

#i = 0
#while i == 0:
#    sleep(1)
#    B.invoke()