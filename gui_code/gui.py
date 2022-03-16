from tkinter import Frame, Label, Button, INSIDE, BOTH, RIGHT, LEFT, Tk
from PIL import Image
from PIL import ImageTk
from matplotlib.animation import FuncAnimation
from matplotlib import style
import time

from profile_page import ProfilePage

style.use("ggplot")

PADDING = 15
GREEN = "#64975E"
AMBER = "#D2A833"
RED = "#C34A4D"
BACKGROUND = "#E7F5EF"
TIME_INTERVAL = 1
TIME_AT_START = time.time()


class FarmBeatsApp:
    def __init__(self, master):
        self.u = 0
        self.main = master
        self.label_frame = Frame(self.main)
        self.label_frame_setup()
        self.option_frame = Frame(self.main, bg="white")
        self.option_frame_setup()
        self.profile_frame = Frame(self.main, bg="white")


    def label_frame_setup(self):
        self.label = Label(self.label_frame, text="IoT FarmBeats", width=60)
        self.label.config(background=BACKGROUND, font=("Courier", 25))
        self.label.pack()
        self.label_frame.pack()

    def get_menu_button(self, image_name):
        width = 240
        height = 220
        img = Image.open(image_name)
        img = img.resize((width, height), Image.ANTIALIAS)
        return ImageTk.PhotoImage(img)

    def option_frame_setup(self):
        for n in range(3):
            self.option_frame.grid_columnconfigure(n, weight=1, uniform="row")

        for n in range(2):
            self.option_frame.grid_rowconfigure(n, weight=1, uniform="row")

        temp_img = self.get_menu_button(
            "assets/optionButtons/temperatureButton.png"
        )

        tempButton = Button(
            self.option_frame,
            image=temp_img,
            command=self.temp_button_action,
            borderwidth=0,
        )

        tempButton.image = temp_img
        tempButton.grid(
            row=0, column=0, sticky="news", pady=PADDING, padx=PADDING
        )

        humidity_img = self.get_menu_button(
            "assets/optionButtons/humidityButton.png"
        )

        humidityButton = Button(
            self.option_frame,
            image=humidity_img,
            command=self.humidity_button_action,
            borderwidth=0,
        )

        humidityButton.image = humidity_img
        humidityButton.grid(
            row=0, column=1, sticky="news", pady=PADDING, padx=PADDING
        )

        brightness_img = self.get_menu_button(
            "assets/optionButtons/brightnessButton.png"
        )

        brightnessButton = Button(
            self.option_frame,
            image=brightness_img,
            command=self.brightness_button_action,
            borderwidth=0,
        )
        brightnessButton.image = brightness_img
        brightnessButton.grid(
            row=0, column=2, sticky="news", pady=PADDING, padx=PADDING
        )

        water_img = self.get_menu_button(
            "assets/optionButtons/waterLevelButton.png"
        )

        waterButton = Button(
            self.option_frame,
            image=water_img,
            command=self.water_button_action,
            borderwidth=0,
        )

        waterButton.image = water_img
        waterButton.grid(
            row=1, column=0, sticky="news", pady=PADDING, padx=PADDING
        )

        aiCamera_img = self.get_menu_button(
            "assets/optionButtons/aiCameraButton.png"
        )

        aiCameraButton = Button(
            self.option_frame,
            image=aiCamera_img,
            command=self.ai_camera_button_action,
            borderwidth=0,
        )

        aiCameraButton.image = aiCamera_img
        aiCameraButton.grid(
            row=1, column=1, sticky="news", pady=PADDING, padx=PADDING
        )

        system_img = self.get_menu_button(
            "assets/optionButtons/systemVisualisationButton.png"
        )

        sysVisualButton = Button(
            self.option_frame,
            image=system_img,
            command=self.sys_visual_button_action,
            borderwidth=0,
        )

        sysVisualButton.image = system_img
        sysVisualButton.grid(
            row=1, column=2, sticky="news", pady=PADDING, padx=PADDING
        )

        self.option_frame.pack(expand=True, fill=BOTH, pady=15, padx=15)  

    def temp_button_action(self):
        self.option_frame.pack_forget()
        ProfilePage("Temperature", self.profile_frame, self.label_frame, self.label, self.option_frame)

    def humidity_button_action(self):
        self.option_frame.pack_forget()
        ProfilePage("Humidity", self.profile_frame, self.label_frame, self.label, self.option_frame)

    def brightness_button_action(self):
        self.option_frame.pack_forget()
        ProfilePage("Brightness", self.profile_frame, self.label_frame, self.label, self.option_frame)

    def water_button_action(self):
        self.is_water = True
        self.option_frame.pack_forget()
        ProfilePage("Water Level", self.profile_frame, self.label_frame, self.label, self.option_frame)

    def ai_camera_button_action(self):
        self.label.config(text="AI Camera Button Clicked")

    def sys_visual_button_action(self):
        self.label.config(text="System Visualisation Button Clicked")


def main():
    root = Tk()
    root.geometry("900x600")
    root.config(bg=BACKGROUND)
    root.resizable(False, False)
    FarmBeatsApp(root)

    root.mainloop()


if __name__ == "__main__":
    main()
