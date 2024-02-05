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
right = C.create_oval(width*3/4-200, height/2-200, width*3/4+200, height/2+200, fill='black')

#Drawing lines for the robot to reorient itself
horizontal = C.create_line(0, height/2, width, height/2)
vertical = C.create_line(width/2, 0, width/2, height)

#Drawing the circle that's supposed to change
value = random.randint(50,400)
left = C.create_oval(width/4-value, height/2-value, width/4+value, height/2+value, fill="black") 

def display_stimulus():
    left = C.create_rectangle(0, 0, width/2, height, fill="white")
    horizontal = C.create_line(0, height/2, width, height/2)
    value = random.randint(50,400)
    left = C.create_oval(width/4-value, height/2-value, width/4+value, height/2+value, fill="black") 

    print("The radius of the new circle is",value,"pixels")

#Programming the button
B = tkinter.Button(top, text ="reset", command=display_stimulus)
B.place(x=0,y=0)

C.pack()
top.mainloop()