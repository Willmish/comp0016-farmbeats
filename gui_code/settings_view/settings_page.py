from tkinter import BOTH, INSIDE, Button, Frame, Label, filedialog
from PIL import Image, ImageTk
from tools.constants import Constants


class SettingsPage:
    def __init__(self, main_frame, title_frame, label, option_frame):
        """__init__ Displays profile page.
        :param settings_frame:
        :type settings_frame: Frame
        :param title_frame:
        :type title_frame: Frame
        :param label:
        :type label: Str
        :param option_frame:
        :type option_frame: Frame
        """

        self.option_frame = option_frame
        self.settings_frame = Frame(main_frame, bg="white")
        self.label_frame = title_frame
        self.label = label
        self.file_info = None
        self.page_setup()

    def page_setup(self):
        """
        profile_setup fills in the profile frame before displaying
        """
        self.label.config(text="System Settings")

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

        for n in range(2):
            self.settings_frame.grid_columnconfigure(n, weight=1)
        for n in range(4):
            self.settings_frame.grid_rowconfigure(n, weight=1)

        plant_name_label = Label(
            self.settings_frame,
            text="The system GUI display takes the values shown\n"
            + "in configuration file below for a specific plant.",
            font=(Constants.FONT_STYLE.value, 15),
        )
        plant_name_label.grid(
            row=0,
            column=0,
            sticky="news",
            pady=Constants.PADDING.value,
            padx=Constants.PADDING.value,
        )

        current_file_frame = Frame(
            self.settings_frame, bg=Constants.BACKGROUND.value
        )

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
            font=(Constants.FONT_STYLE.value, 15),
        )
        self.file_info.pack()

        current_file_frame.grid(
            row=1, column=0, sticky="news", pady=25, padx=25, rowspan=3
        )

        change_file_button = Button(
            self.settings_frame,
            text="Change File",
            command=self.change_file_action,
        )
        change_file_button.grid(
            row=1,
            column=1,
            sticky="news",
            pady=25,
            padx=25,
        )

        self.settings_frame.pack(
            fill=BOTH,
            expand=True,
            pady=Constants.PADDING.value,
            padx=Constants.PADDING.value,
        )

    def change_file_action(self):
        path = filedialog.askopenfilename()
        if len(path) > 0:
            with open(path, "r") as input:
                with open("tools/plant_profile_info.ini", "w+") as f:
                    f.write(input.read())
                    print(f.read())
        with open("tools/plant_profile_info.ini", "r") as f:
            self.file_info.config(text=f.read())

    def home_button_action(self, binst):
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
