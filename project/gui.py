
from tkinter import *
from turtle import home

PADDING = 25
INPUT = 900

class FarmBeatsApp:

    def __init__(self, master):
        self.main = master
        self.labelFrame = Frame(self.main)
        self.labelFrameSetUp()
        self.optionFrame = Frame(self.main, bg='white')
        self.optionFrameSetUp()
        self.profileFrame = Frame(self.main, bg='white')
        

    def labelFrameSetUp(self):
        self.label = Label(self.labelFrame, text = "IoT FarmBeats", width=60)
        self.label.config(background = '#E7F5EF') #E7F5EF
        self.label.config(font=("Courier", 25))
        self.label.pack()
        self.labelFrame.pack()

    def optionFrameSetUp(self):
        for n in range(3):
            self.optionFrame.grid_columnconfigure(n, weight=1)
        
        for n in range(2):
            self.optionFrame.grid_rowconfigure(n, weight=1)

        tempButton = Button(self.optionFrame, text = "Temperature", command = self.tempButtonAction)
        tempButton['font'] = "Courier"
        tempButton.grid(row = 0, column = 0, sticky = 'news', pady = PADDING, padx = PADDING)

        humidityButton = Button(self.optionFrame, text = "Humidity", command = self.humidityButtonAction)
        humidityButton['font'] = "Courier"
        humidityButton.grid(row = 0, column = 1, sticky = 'news', pady = PADDING, padx = PADDING)

        brightnessButton = Button(self.optionFrame, text = "Brightness", command = self.brightnessButtonAction)
        brightnessButton['font'] = "Courier"
        brightnessButton.grid(row = 0, column = 2, sticky = 'news', pady = PADDING, padx = PADDING)

        waterButton = Button(self.optionFrame, text = "Water Level", command = self.waterButtonAction )
        waterButton['font'] = "Courier"
        waterButton.grid(row = 1, column = 0, sticky = 'news', pady = PADDING, padx = PADDING)

        aiCameraButton = Button(self.optionFrame, text = "AI Camera", command = self.aiCameraButtonAction)
        aiCameraButton['font'] = "Courier"
        aiCameraButton.grid(row = 1, column = 1, sticky = 'news', pady = PADDING, padx = PADDING)

        sysVisualButton = Button(self.optionFrame, text = "System Visualisation", command = self.sysVisualButtonAction)
        sysVisualButton['font'] = "Courier"
        sysVisualButton.grid(row = 1, column = 2, sticky = 'news', pady = PADDING, padx = PADDING)

        self.optionFrame.pack(expand=True, fill=BOTH, pady = 15, padx = 15)

    def profileFrameSetUp(self):
        #sensorFrame set up
        sensorFrame = Frame(self.profileFrame, bg = '#E7F5EF')
        for n in range(2):
            self.profileFrame.grid_columnconfigure(n, weight=1)
        self.profileFrame.grid_rowconfigure(0, weight=1)
        sensorFrame.grid(row = 0, column = 0, sticky = 'news', pady = PADDING, padx = PADDING)

        sensorTitle = Label(sensorFrame, text = "Light Sensor Information")
        sensorTitle.config(background = '#E7F5EF') #E7F5EF
        sensorTitle.config(font=("Courier", 15))
        sensorTitle.pack()

        value = Label(sensorFrame, text = "Current value: " + str(INPUT) + "cd")
        value.config(background = '#E7F5EF') #E7F5EF
        value.config(font=("Courier", 15))
        value.pack()
        currVal = DoubleVar()
        currVal.set(INPUT)
        s1 = Scale( sensorFrame, variable = currVal, from_ = 0, to = 1000, orient = HORIZONTAL, state = 'disabled') 
        s1.pack()
        
        #actuatorFrame set up

        # display on profileFrame
        self.profileFrame.pack(fill = BOTH, expand = True, pady = 15, padx = 15)
    


    def homeButtonAction(self, binst):
        self.profileFrame.pack_forget()
        self.optionFrame.pack(expand=True, fill=BOTH, pady = 15, padx = 15) 
        binst.destroy()
        self.label.config(text = "IoT FarmBeats")

    def tempButtonAction(self):
        self.label.config(text = 'Temperature Button Clicked')

    def humidityButtonAction(self):
        self.label.config(text = 'Humidity Button Clicked')
    
    def brightnessButtonAction(self):
        self.label.config(text = "Brightness")
        homeButton = Button(self.labelFrame, text = "Home")
        homeButton['command'] = lambda idx="Home", binst=homeButton: self.homeButtonAction(binst)
        homeButton.pack()
        homeButton.place(bordermode=INSIDE, x= 5, y=5)
        self.optionFrame.pack_forget()
        self.profileFrameSetUp()

    
    def waterButtonAction(self):
        self.label.config(text = 'Water Level Button Clicked')

    def aiCameraButtonAction(self):
        self.label.config(text = 'AI Camera Button Clicked')
    
    def sysVisualButtonAction(self):
        self.label.config(text = 'System Visualisation Button Clicked')

            
def main():            
    root = Tk()
    root.geometry("1000x600")
    root.config(bg='#E7F5EF')
    app = FarmBeatsApp(root)
    root.mainloop()
    
if __name__ == "__main__": main()
