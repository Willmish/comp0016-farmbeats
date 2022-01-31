
from tkinter import *
from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

PADDING = 25

#dummy constants for sensor profile
INPUT = 800

LOWER = 700
UPPER = 850
EXLOWER = 600
EXUPPER = 950
ACTUATION = 900
MESSAGE = "The brightness level is good!"

TIMELIST = [0,5,10,15,20,25,30,35,40,45]
VALUELIST = [904,920, 911, 890, 883,880,881, 860, 872, 888]

GREEN = '#64975E'
AMBER = '#D2A833'
RED = '#C34A4D'

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
        self.label.config(background = '#E7F5EF', font=("Courier", 25)) #E7F5EF
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

        for n in range(2):
            self.profileFrame.grid_columnconfigure(n, weight=1)
        for n in range(4):
            self.profileFrame.grid_rowconfigure(n, weight=1)
        
        #sensorFrame set up
        sensorFrame = Frame(self.profileFrame, bg = '#E7F5EF')

        sensorTitle = Label(sensorFrame, text = "Light Sensor Information")
        sensorTitle.config(background = '#E7F5EF', font=("Courier", 15)) #E7F5EF
        sensorTitle.pack()

        value = Label(sensorFrame, text = "Current value: " + str(INPUT) + "cd")
        value.config(background = '#E7F5EF') #E7F5EF
        value.config(font=("Courier", 15))
        value.pack()
        currVal = DoubleVar()
        currVal.set(INPUT)

        subFrame = Frame(sensorFrame, bg = '#E7F5EF')
        s1 = Scale( subFrame, variable = currVal, sliderlength= 5, from_ = 0, to = 1000, orient = HORIZONTAL, state = 'disabled', background = '#E7F5EF') 
        s1.pack(side = LEFT)

        colour = self.getColour(INPUT, EXUPPER, EXLOWER, UPPER, LOWER)
        colourFrame = Frame(subFrame, bg = colour, width= 30, height= 30)
        colourFrame.pack(side = RIGHT)
        subFrame.pack()
        self.graphDisplay(sensorFrame)
        sensorFrame.grid(row = 0, column = 0, sticky = 'news', pady = PADDING, padx = PADDING, rowspan=4)

        
        #actuatorFrame set up

        actuatorFrame = Frame(self.profileFrame, bg = '#E7F5EF')
        actuatorTitle = Label(actuatorFrame, text = "LED light Information")
        actuatorTitle.config(background = '#E7F5EF', font=("Courier", 15)) #E7F5EF
        actuatorTitle.pack()

        modeSwitchFrame = Frame(actuatorFrame, bg = '#E7F5EF')
        manualMode = Label(modeSwitchFrame, text = "Manual")
        manualMode.config(background = '#CEE5DB', font=("Courier", 15)) #E7F5EF
        manualMode.pack(side = RIGHT)
        automaticMode = Button(modeSwitchFrame, text = "Automatic")
        automaticMode.config(background = '#E7F5EF', font=("Courier", 15)) #E7F5EF
        automaticMode.pack(side = LEFT)
        modeSwitchFrame.pack()


        actuatorVal = Label(actuatorFrame, text = "Brightness set to: "+ str(ACTUATION) + "cd")
        actuatorVal.config(background = '#E7F5EF', font=("Courier", 15)) #E7F5EF
        actuatorVal.pack()
        

        actuatorFrame.grid(row = 0, column = 1, sticky = 'news', pady = PADDING, padx = PADDING, rowspan=3)


        #suggestionFrame set up

        suggestionFrame = Frame(self.profileFrame, bg = '#E7F5EF')
        suggestionLabel = Label(suggestionFrame, text = "Suggestion")
        suggestionLabel.config(background = '#E7F5EF', font=("Courier", 15)) #E7F5EF
        suggestionLabel.pack()
        messageFrame = Frame(suggestionFrame, bg = '#FFFFFF', height=400)
        msg = Label(messageFrame, text = MESSAGE)
        msg.pack()
        messageFrame.pack()


        suggestionFrame.grid(row = 3, column = 1, sticky = 'news', pady = PADDING, padx = PADDING)


        # display on profileFrame

        self.profileFrame.pack(fill = BOTH, expand = True, pady = 15, padx = 15)
    
    def getColour(self, val, extrUpper, extrLower, upper, lower):
        if val <= upper and val >= lower:
            return GREEN
        elif (val <= extrUpper and val > upper) or (val <= extrLower and val > lower):
            return AMBER
        else:
            return RED

    def graphDisplay(self,  frame ):
        dataFrame = DataFrame({'Time (ms)': TIMELIST,'Brightness (cd)': VALUELIST}, columns=['Time (ms)', 'Brightness (cd)'])
        fig = plt.Figure(figsize=(5,4), dpi=100)
        ax = fig.add_subplot(111)
        FigureCanvasTkAgg(fig, frame).get_tk_widget().pack(pady = 15, padx = 15)
        dataFrame = dataFrame[['Time (ms)', 'Brightness (cd)']].groupby('Time (ms)').sum()
        dataFrame.plot(kind='line', legend=True, ax=ax, color='r',marker='o', fontsize=10)
        ax.set_title('Brightness from Sensor over Time')


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
