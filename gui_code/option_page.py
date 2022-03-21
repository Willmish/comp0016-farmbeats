from tkinter import Button, BOTH
from PIL import Image
from PIL import ImageTk
from constants import Constants
from profile_page import ProfilePage


class OptionPage:
    def __init__(self, option_frame, profile_frame, label_frame, label):
        self.option_frame = option_frame
        self.profile_frame = profile_frame
        self.label_frame = label_frame
        self.label = label

        self.option_frame_setup()

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
            row=0,
            column=0,
            sticky="news",
            pady=Constants.PADDING.value,
            padx=Constants.PADDING.value,
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
            row=0,
            column=1,
            sticky="news",
            pady=Constants.PADDING.value,
            padx=Constants.PADDING.value,
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
            row=0,
            column=2,
            sticky="news",
            pady=Constants.PADDING.value,
            padx=Constants.PADDING.value,
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
            row=1,
            column=0,
            sticky="news",
            pady=Constants.PADDING.value,
            padx=Constants.PADDING.value,
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
            row=1,
            column=1,
            sticky="news",
            pady=Constants.PADDING.value,
            padx=Constants.PADDING.value,
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
            row=1,
            column=2,
            sticky="news",
            pady=Constants.PADDING.value,
            padx=Constants.PADDING.value,
        )

        self.option_frame.pack(expand=True, fill=BOTH, pady=15, padx=15)

    def get_menu_button(self, image_name):
        width = 240
        height = 220
        img = Image.open(image_name)
        img = img.resize((width, height), Image.ANTIALIAS)
        return ImageTk.PhotoImage(img)

    def temp_button_action(self):
        self.option_frame.pack_forget()
        ProfilePage(
            "Temperature",
            self.profile_frame,
            self.label_frame,
            self.label,
            self.option_frame,
        )

    def humidity_button_action(self):
        self.option_frame.pack_forget()
        ProfilePage(
            "Humidity",
            self.profile_frame,
            self.label_frame,
            self.label,
            self.option_frame,
        )

    def brightness_button_action(self):
        self.option_frame.pack_forget()
        ProfilePage(
            "Brightness",
            self.profile_frame,
            self.label_frame,
            self.label,
            self.option_frame,
        )

    def water_button_action(self):
        self.is_water = True
        self.option_frame.pack_forget()
        ProfilePage(
            "Water Level",
            self.profile_frame,
            self.label_frame,
            self.label,
            self.option_frame,
        )

    def ai_camera_button_action(self):
        self.label.config(text="AI Camera Button Clicked")

    def sys_visual_button_action(self):
        self.label.config(text="System Visualisation Button Clicked")
