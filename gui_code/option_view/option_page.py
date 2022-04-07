from tkinter import Button, BOTH, Frame
from PIL import Image
from PIL import ImageTk
from tools.constants import Constants
from profile_view.profile_page import ProfilePage
from settings_view.settings_page import SettingsPage
from data_streamer.gui_database_manager import GuiDatabaseManager


class OptionPage:
    """
    OptionPage displays option_frame that contains buttons
    for each subsystem as well as extra features like AI
    camera and System Settings.
    """

    def __init__(
        self,
        main_frame,
        title_frame,
        label,
        db: GuiDatabaseManager,
    ):
        """
        __init__ creates an instance of OptionPage.

        :param main_frame: Parent frame of option_frame.
        :type main_frame: Frame
        :param title_frame: A frame that displays setting page
            title as well as home button.
        :type title_frame: Frame
        :param label: Label to be added to title_frame.
        :type label: Label
        :param db: Instance of GuiDatabaseManager used to
            communicate with the azure database.
        :type db: GuiDatabaseManager
        """
        self.main_frame = main_frame
        self.option_frame = Frame(main_frame, bg="white")
        self.title_frame = title_frame
        self.label = label
        self._db_manager: GuiDatabaseManager = db

        self.option_frame_setup()

    def option_frame_setup(self):
        """
        option_frame_setup fills the option_frame with a button
        for each subsystem and additional features.
        """
        for n in range(3):
            self.option_frame.grid_columnconfigure(n, weight=1, uniform="row")

        for n in range(2):
            self.option_frame.grid_rowconfigure(n, weight=1, uniform="row")

        temp_img = self.get_menu_button(
            "assets/optionButtons/temperatureButton.png"
        )
        temp_button = Button(
            self.option_frame,
            image=temp_img,
            command=self.temp_button_action,
            borderwidth=0,
        )
        temp_button.image = temp_img
        temp_button.grid(
            row=0,
            column=0,
            sticky="news",
            pady=Constants.PADDING.value,
            padx=Constants.PADDING.value,
        )

        humidity_img = self.get_menu_button(
            "assets/optionButtons/humidityButton.png"
        )
        humidity_button = Button(
            self.option_frame,
            image=humidity_img,
            command=self.humidity_button_action,
            borderwidth=0,
        )
        humidity_button.image = humidity_img
        humidity_button.grid(
            row=0,
            column=1,
            sticky="news",
            pady=Constants.PADDING.value,
            padx=Constants.PADDING.value,
        )

        brightness_img = self.get_menu_button(
            "assets/optionButtons/brightnessButton.png"
        )
        brightness_button = Button(
            self.option_frame,
            image=brightness_img,
            command=self.brightness_button_action,
            borderwidth=0,
        )
        brightness_button.image = brightness_img
        brightness_button.grid(
            row=0,
            column=2,
            sticky="news",
            pady=Constants.PADDING.value,
            padx=Constants.PADDING.value,
        )

        soil_moisture_img = self.get_menu_button(
            "assets/optionButtons/soilMoistureButton.png"
        )
        soil_moisture_button = Button(
            self.option_frame,
            image=soil_moisture_img,
            command=self.soil_moisture_button_action,
            borderwidth=0,
        )

        soil_moisture_button.image = soil_moisture_img
        soil_moisture_button.grid(
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
            "assets/optionButtons/systemSettingsButton.png"
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

    def get_menu_button(self, image_name) -> ImageTk.PhotoImage:
        """
        get_menu_button gets and resizes the image based on image_name.

        :param image_name: Name of image file.
        :type image_name: str
        :return: Resized image of the type ImageTk.PhotoImage.
        :rtype: ImageTk.PhotoImage
        """
        width = 240
        height = 220
        img = Image.open(image_name)
        img = img.resize((width, height), Image.ANTIALIAS)
        return ImageTk.PhotoImage(img)

    def temp_button_action(self):
        """
        temp_button_action creates a profile page for the
        temperature subsystem and swaps out the option_frame.
        """
        self.option_frame.pack_forget()
        ProfilePage(
            "Temperature",
            self.main_frame,
            self.title_frame,
            self.label,
            self.option_frame,
            self._db_manager,
        )

    def humidity_button_action(self):
        """
        humidity_button_action creates a profile page for the
        humidity subsystem and swaps out the option_frame.
        """
        self.option_frame.pack_forget()
        ProfilePage(
            "Humidity",
            self.main_frame,
            self.title_frame,
            self.label,
            self.option_frame,
            self._db_manager,
        )

    def brightness_button_action(self):
        """
        brightness_button_action creates a profile page for the
        brightness subsystem and swaps out the option_frame.
        """
        self.option_frame.pack_forget()
        ProfilePage(
            "Brightness",
            self.main_frame,
            self.title_frame,
            self.label,
            self.option_frame,
            self._db_manager,
        )

    def soil_moisture_button_action(self):
        """
        soil_moisture_button_action creates a profile page for the
        soil moisture subsystem and swaps out the option_frame.
        """
        self.is_water = True
        self.option_frame.pack_forget()
        ProfilePage(
            "Soil Moisture",
            self.main_frame,
            self.title_frame,
            self.label,
            self.option_frame,
            self._db_manager,
        )

    def ai_camera_button_action(self):
        """
        ai_camera_button_action should be where the AI Camera
        page is going to be. This has yet to be implemented.
        """
        self.label.config(text="AI Camera Button Clicked")

    def sys_visual_button_action(self):
        """
        sys_visual_button_action creates a settings page and swaps
        out the option_frame.
        """
        self.option_frame.pack_forget()
        SettingsPage(
            self.main_frame, self.title_frame, self.label, self.option_frame
        )
