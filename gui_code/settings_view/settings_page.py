from tkinter import (
    BOTH,
    INSIDE,
    NW,
    Button,
    Canvas,
    Frame,
    Label,
    filedialog,
)
from PIL import Image, ImageTk
from tools.config_file_parser import ConfigFileParser
from tools.constants import Constants


class SettingsPage:
    """
    SettingsPage creates a frame that contains all components that can
    allow the user to view or change current configuration file.
    """

    def __init__(
        self,
        main_frame: Frame,
        title_frame: Frame,
        label: Label,
        option_frame: Frame,
    ):
        """__init__ creates an instance of SettingsPage.

        :param main_frame: Parent frame of option_frame.
        :type main_frame: Frame
        :param title_frame: A frame that displays setting page
            title as well as home button.
        :type title_frame: Frame
        :param label: Label to be added to title_frame, showing page title.
        :type label: Label
        :param option_frame: Option frame, allowing SettingsPage to
            go back when home button is pressed.
        :type option_frame: Frame
        """

        self.option_frame = option_frame
        self.settings_frame = Frame(main_frame, bg="white")
        self.label_frame = title_frame
        self.label = label
        self.file_info = None
        self.message = None
        self.page_setup()

    def page_setup(self):
        """
        page_setup fills in the settings_frame with description labels,
        current configuration file and button for changing current
        configuration file. It also adds home button to label_frame
        for user to navigate back to option page.
        """
        self.label.config(text="System Settings")

        # Home button

        img = Image.open("assets/homeIcon.png")
        home_icon = ImageTk.PhotoImage(img)

        home_button = Button(self.label_frame, image=home_icon, borderwidth=0)
        home_button.image = home_icon

        home_button[
            "command"
        ] = lambda idx="Home", binst=home_button: self.home_button_action(
            binst
        )

        home_button.pack()
        home_button.place(bordermode=INSIDE, x=5, y=5)

        # settings_frame set up
        self.settings_frame.grid_columnconfigure(0, weight=1)
        self.settings_frame.grid_columnconfigure(0, weight=1)
        self.settings_frame.grid_columnconfigure(1, weight=1)

        Frame(self.settings_frame).grid(row=0, column=1)

        left_frame = Frame(self.settings_frame)

        section_title_label = Label(
            left_frame,
            text="Plant Profile Settings",
            font=(Constants.FONT_STYLE.value, 25),
        )
        section_title_label.pack(pady=15)

        description_label = Label(
            left_frame,
            text="The system GUI display takes the values shown\n"
            + "in configuration file below for a specific plant.",
            font=(Constants.FONT_STYLE.value, 15),
        )
        description_label.pack(pady=15)

        current_file_frame = Frame(left_frame, bg=Constants.BACKGROUND.value)

        frame_title = Label(
            current_file_frame,
            text="Current config file:",
            font=(Constants.FONT_STYLE.value, 15),
            background=Constants.BACKGROUND.value,
        )
        frame_title.pack()
        with open("tools/plant_profile_info.ini", "r") as file:
            read_string = file.read()
        self.file_info = Label(
            current_file_frame,
            text=read_string,
            font=(Constants.FONT_STYLE.value, 13),
        )
        self.file_info.pack()

        change_file_button = Button(
            current_file_frame,
            bg=Constants.BACKGROUND.value,
            text="Change File",
            command=self.change_file_action,
            padx=15,
            pady=15,
        )
        change_file_button.pack()

        current_file_frame.pack()

        self.message = Label(
            left_frame, text="", font=(Constants.FONT_STYLE.value, 15)
        )
        self.message.pack()
        left_frame.grid(
            row=0,
            column=1,
            sticky="news",
            pady=Constants.PADDING.value,
        )

        canvas = Canvas(self.settings_frame, width=500, height=600)

        img = Image.open("assets/settingsPagePlant.png")
        new_img = ImageTk.PhotoImage(img.resize((300, 500), Image.ANTIALIAS))
        canvas.create_image(0, 0, anchor=NW, image=new_img)
        canvas.image = new_img
        canvas.grid(
            row=0,
            column=2,
            sticky="news",
            pady=25,
        )

        self.settings_frame.pack(
            fill=BOTH,
            expand=True,
            pady=Constants.PADDING.value,
            padx=Constants.PADDING.value,
        )

    def change_file_action(self):
        """
        change_file_action allows user to select file to
        be copied into tools/plant_profile_info.ini.
        """
        path = filedialog.askopenfilename()
        if len(path) > 0:
            with open(path, "r") as input:
                if ConfigFileParser(path).valid:
                    with open("tools/plant_profile_info.ini", "w+") as f:
                        f.write(input.read())
                        print(f.read())
                        with open("tools/plant_profile_info.ini", "r") as f2:
                            self.file_info.config(text=f2.read())
                        self.message.config(text="File change successful.")

                else:
                    self.message.config(text="Error. Cannot change file.")
                    print("CANNOT CHANGE FILE")

    def home_button_action(self, binst: Button):
        """
        home_button_action allows the settings_frame to be
        replaced by option_frame, taking user back to option page.

        :param binst: The home button itself.
        :type binst: Button
        """
        self.is_water = False
        self.settings_frame.pack_forget()
        self.option_frame.pack(
            expand=True,
            fill=BOTH,
            pady=Constants.PADDING.value,
            padx=Constants.PADDING.value,
        )
        binst.destroy()
        self.label.config(text="IoT FarmBeats")
