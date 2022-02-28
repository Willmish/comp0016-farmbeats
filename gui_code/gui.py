from tkinter import Frame, Label, Button, INSIDE, BOTH, RIGHT, LEFT, Tk
import tkinter
from pandas import DataFrame
import matplotlib.pyplot as plt
from profileInformation import ProfileInformation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image
from PIL import ImageTk

PADDING = 25

GREEN = "#64975E"
AMBER = "#D2A833"
RED = "#C34A4D"
BACKGROUND = "#E7F5EF"


class FarmBeatsApp:
    def __init__(self, master):
        self.main = master
        self.labelFrame = Frame(self.main)
        self.labelFrameSetUp()
        self.optionFrame = Frame(self.main, bg="white")
        self.optionFrameSetUp()
        self.profileFrame = Frame(self.main, bg="white")

    def labelFrameSetUp(self):

        self.label = Label(self.labelFrame, text="IoT FarmBeats", width=60)
        self.label.config(background=BACKGROUND, font=("Courier", 25))
        self.label.pack()
        self.labelFrame.pack()

    def getMenuButton(self, imageName):
        width = 240
        height = 220
        img = Image.open(imageName)
        img = img.resize((width, height), Image.ANTIALIAS)
        return ImageTk.PhotoImage(img)

    def optionFrameSetUp(self):
        for n in range(3):
            self.optionFrame.grid_columnconfigure(n, weight=1, uniform="row")

        for n in range(2):
            self.optionFrame.grid_rowconfigure(n, weight=1, uniform="row")

        tempImg = self.getMenuButton(
            "assets/optionButtons/temperatureButton.png"
        )

        tempButton = Button(
            self.optionFrame,
            image=tempImg,
            command=self.tempButtonAction,
            borderwidth=0,
        )

        tempButton.image = tempImg
        tempButton.grid(
            row=0, column=0, sticky="news", pady=PADDING, padx=PADDING
        )

        humidityImg = self.getMenuButton(
            "assets/optionButtons/humidityButton.png"
        )

        humidityButton = Button(
            self.optionFrame,
            image=humidityImg,
            command=self.humidityButtonAction,
            borderwidth=0,
        )

        humidityButton.image = humidityImg
        humidityButton.grid(
            row=0, column=1, sticky="news", pady=PADDING, padx=PADDING
        )

        brightnessImg = self.getMenuButton(
            "assets/optionButtons/brightnessButton.png"
        )

        brightnessButton = Button(
            self.optionFrame,
            image=brightnessImg,
            command=self.brightnessButtonAction,
            borderwidth=0,
        )
        brightnessButton.image = brightnessImg
        brightnessButton.grid(
            row=0, column=2, sticky="news", pady=PADDING, padx=PADDING
        )

        waterImg = self.getMenuButton(
            "assets/optionButtons/waterLevelButton.png"
        )

        waterButton = Button(
            self.optionFrame,
            image=waterImg,
            command=self.waterButtonAction,
            borderwidth=0,
        )

        waterButton.image = waterImg
        waterButton.grid(
            row=1, column=0, sticky="news", pady=PADDING, padx=PADDING
        )

        aiCameraImg = self.getMenuButton(
            "assets/optionButtons/aiCameraButton.png"
        )

        aiCameraButton = Button(
            self.optionFrame,
            image=aiCameraImg,
            command=self.aiCameraButtonAction,
            borderwidth=0,
        )

        aiCameraButton.image = aiCameraImg
        aiCameraButton.grid(
            row=1, column=1, sticky="news", pady=PADDING, padx=PADDING
        )

        systemImg = self.getMenuButton(
            "assets/optionButtons/systemVisualisationButton.png"
        )

        sysVisualButton = Button(
            self.optionFrame,
            image=systemImg,
            command=self.sysVisualButtonAction,
            borderwidth=0,
        )

        sysVisualButton.image = systemImg
        sysVisualButton.grid(
            row=1, column=2, sticky="news", pady=PADDING, padx=PADDING
        )

        self.optionFrame.pack(expand=True, fill=BOTH, pady=15, padx=15)

    def profileSetUp(self, profileName):

        profile = ProfileInformation(profileName)
        self.label.config(text=profile.title)
        img = Image.open("assets/homeIcon.png")
        homeIcon = ImageTk.PhotoImage(img)

        homeButton = Button(self.labelFrame, image=homeIcon, borderwidth=0)
        homeButton.image = homeIcon

        homeButton[
            "command"
        ] = lambda idx="Home", binst=homeButton: self.homeButtonAction(binst)
        homeButton.pack()
        homeButton.place(bordermode=INSIDE, x=5, y=5)

        for n in range(2):
            self.profileFrame.grid_columnconfigure(n, weight=1)
        for n in range(4):
            self.profileFrame.grid_rowconfigure(n, weight=1)

        # SensorFrame set up

        sensorFrame = Frame(self.profileFrame, bg=BACKGROUND)

        sensorTitle = Label(sensorFrame, text=profile.sensorFrameTitle)
        sensorTitle.config(background=BACKGROUND, font=("Courier", 15))
        sensorTitle.pack()

        value = Label(sensorFrame, text=profile.sensorValueDescription)
        value.config(background=BACKGROUND)
        value.config(font=("Courier", 15))
        value.pack()

        subFrame = Frame(sensorFrame, bg=BACKGROUND)

        range_ = profile.bound[1] - profile.bound[0]
        l1 = ((profile.extr[0] - profile.bound[0]) / range_) * 400
        l2 = ((profile.extr[1] - profile.bound[0]) / range_) * 400
        l3 = ((profile.extr[2] - profile.bound[0]) / range_) * 400
        l4 = ((profile.extr[3] - profile.bound[0]) / range_) * 400

        line = ((profile.sensorValue - profile.bound[0]) / range_) * 400
        scaleCanvas = tkinter.Canvas(subFrame, height=40, width=400)

        scaleCanvas.create_rectangle(0, 0, l1, 30, fill=RED, width=0)
        scaleCanvas.create_rectangle(l1, 0, l2, 30, fill=AMBER, width=0)
        scaleCanvas.create_rectangle(l2, 0, l3, 30, fill=GREEN, width=0)
        scaleCanvas.create_rectangle(l3, 0, l4, 30, fill=AMBER, width=0)
        scaleCanvas.create_rectangle(l4, 0, 400, 30, fill=RED, width=0)
        scaleCanvas.create_line(0, 15, line, 15, width=3)
        scaleCanvas.pack()

        subFrame.pack()
        self.graphDisplay(sensorFrame, profile)
        sensorFrame.grid(
            row=0,
            column=0,
            sticky="news",
            pady=PADDING,
            padx=PADDING,
            rowspan=4,
        )

        # ActuatorFrame set up

        actuatorFrame = Frame(self.profileFrame, bg=BACKGROUND)
        actuatorFrame.grid_columnconfigure(0, weight=1)
        for n in range(3):
            actuatorFrame.grid_rowconfigure(n, weight=1)
        actuatorTitle = Label(actuatorFrame, text=profile.actuatorFrameTitle)
        actuatorTitle.config(background=BACKGROUND, font=("Courier", 15))

        actuatorTitle.grid(
            row=0, column=0, sticky="news", pady=PADDING, padx=PADDING
        )

        modeSwitchFrame = Frame(actuatorFrame, bg=BACKGROUND)
        manualMode = Label(modeSwitchFrame, text="Manual")
        manualMode.config(background="#CEE5DB", font=("Courier", 15))
        manualMode.pack(side=RIGHT)
        automaticMode = Button(modeSwitchFrame, text="Automatic")
        automaticMode.config(background=BACKGROUND, font=("Courier", 15))
        automaticMode.pack(side=LEFT)

        modeSwitchFrame.grid(
            row=1, column=0, sticky="news", pady=PADDING, padx=PADDING
        )

        actuatorVal = Label(
            actuatorFrame, text=profile.actuatorValueDescription
        )

        actuatorVal.config(background=BACKGROUND, font=("Courier", 15))

        actuatorVal.grid(
            row=2, column=0, sticky="news", pady=PADDING, padx=PADDING
        )

        actuatorFrame.grid(
            row=0,
            column=1,
            sticky="news",
            pady=PADDING,
            padx=PADDING,
            rowspan=3,
        )

        # SuggestionFrame set up

        suggestionFrame = Frame(self.profileFrame, bg="#E7F5EF")
        suggestionLabel = Label(suggestionFrame, text="Suggestion")
        suggestionLabel.config(background="#E7F5EF", font=("Courier", 15))
        suggestionLabel.pack()
        messageFrame = Frame(suggestionFrame, bg="#FFFFFF", height=400)
        msg = Label(messageFrame, text=profile.suggestion)
        msg.pack()
        messageFrame.pack()

        suggestionFrame.grid(
            row=3, column=1, sticky="news", pady=PADDING, padx=PADDING
        )

        # Display on profileFrame

        self.profileFrame.pack(fill=BOTH, expand=True, pady=15, padx=15)

    def getColour(self, val, extrLower, lower, upper, extrUpper):
        if val <= upper and val >= lower:
            return GREEN
        elif val <= extrUpper and val > upper:
            return AMBER
        elif val <= extrLower and val > lower:
            return AMBER
        else:
            return RED

    def graphDisplay(self, frame, profile):
        print(profile.title)
        print("Timelist: ")
        print(profile.timeList)
        print("Val list: ")
        print(profile.valList)

        y_label = profile.title + " (" + profile.unit + ")"

        dataFrame = DataFrame(
            {"Time (ms)": profile.timeList, y_label: profile.valList},
            columns=["Time (ms)", y_label],
        )

        fig = plt.Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        FigureCanvasTkAgg(fig, frame).get_tk_widget().pack(pady=15, padx=15)
        dataFrame = (
            dataFrame[["Time (ms)", y_label]].groupby("Time (ms)").sum()
        )

        dataFrame.plot(
            linewidth=0.5,
            kind="line",
            legend=True,
            ax=ax,
            color="r",
            fontsize=10,
        )

        ax.set(xlabel="Time (ms)", ylabel=y_label, title=profile.graphTitle)

    def homeButtonAction(self, binst):
        self.profileFrame.pack_forget()
        self.optionFrame.pack(expand=True, fill=BOTH, pady=15, padx=15)
        binst.destroy()
        self.label.config(text="IoT FarmBeats")

    def tempButtonAction(self):
        self.optionFrame.pack_forget()
        self.profileSetUp("Temperature")

    def humidityButtonAction(self):
        self.optionFrame.pack_forget()
        self.profileSetUp("Humidity")

    def brightnessButtonAction(self):
        self.optionFrame.pack_forget()
        self.profileSetUp("Brightness")

    def waterButtonAction(self):
        self.optionFrame.pack_forget()
        self.profileSetUp("Water")

    def aiCameraButtonAction(self):
        self.label.config(text="AI Camera Button Clicked")

    def sysVisualButtonAction(self):
        self.label.config(text="System Visualisation Button Clicked")


def main():
    root = Tk()
    root.geometry("900x600")
    root.config(bg="#E7F5EF")
    root.resizable(False, False)
    FarmBeatsApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
