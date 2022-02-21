# Import the required libraries
from tkinter import *

#Create an instance of tkinter frame
root=Tk()

# Set the geometry of frame
root.geometry("700x350")

# Create a canvas widget
canvas= Canvas(root, bd=2, highlightthickness=2)
canvas.pack(side=TOP, padx=10, pady=10)

# Create an Entry widget
text=Entry(canvas, width=50)
text.insert(0, "Widget with border")
text.config(borderwidth=5)
text.pack(side=TOP, padx=10, pady=10)

# Create Entry widget without border
text=Entry(canvas, width=50)
text.insert(0, "Widget without border")
text.pack(side=TOP, padx=10, pady=10)

label1 = Label(canvas, text="Label with border", borderwidth=2, relief='solid', font="Calibri, 14")
label1.pack(side=BOTTOM, padx=10, pady=10)

label2 = Label(canvas, text="Label without border", borderwidth=0, font="Calibri, 14")
label2.pack(side=BOTTOM, padx=10, pady=10)

button1 = Button(root, text="Standard Button")
button1.pack(side=TOP, padx=10, pady=10)

button2 = Button(root, text="Button without Border", borderwidth=0)
button2.pack(side=TOP, padx=10, pady=10)

root.mainloop()