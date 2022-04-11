from datetime import timedelta
from tkinter import CENTER, NW, TOP, Canvas, Frame, Label, Button, INSIDE, BOTH, RIGHT, LEFT
from typing import List
import matplotlib.pyplot as plt
from profile_view.water_scale import WaterScale
from profile_view.sensor_value_scale import SensorValueScale
from profile_view.profile_information import ProfileInformation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
from matplotlib.animation import FuncAnimation
import time
from tools.constants import Constants
from data_streamer.gui_database_manager import GuiDatabaseManager


class ProfilePage:
    """
    Displays profile page with live updated sensor,
    actuator and suggestion frames.
    """

    NO_XTICKS = 4
    NUM_OF_DATA = 20

    def __init__(
        self,
        profile_name: str,
        main_frame: Frame,
        title_frame: Frame,
        label: Label,
        option_frame: Frame,
        db: GuiDatabaseManager,
    ):

        """
        __init__ creates an instance of ProfilePage.

        :param profile_name: Name of selected subsystem.
        :type profile_name: str
        :param main_frame: Parent frame of option_frame.
        :type main_frame: Frame
        :param title_frame: A frame that displays setting page
            title as well as home button.
        :type title_frame: Frame
        :param label: Label to be added to title_frame.
            showing page title.
        :type label: str
        :param option_frame: Option frame, allowing SettingsPage to
            go back when home button is pressed.
        :type option_frame: Frame
        :param db: Instance of GuiDatabaseManager used to
            communicate with the azure database.
        :type db: GuiDatabaseManager
        """

        self.profile = ProfileInformation(profile_name, db)
        self.option_frame = option_frame
        self.profile_frame = Frame(main_frame, bg="white")
        self.label_frame = title_frame
        self.label = label
        self._db_manager: GuiDatabaseManager = db

        self.sensor_frame = None
        self.curr_sensor_value_label = None
        self.curr_actuator_value_label = None
        self.actuator_frame = None
        self.suggestion_frame = None

        if profile_name == "Soil Moisture":
            self.is_water = True
        else:
            self.is_water = False

        self.time_since_update = time.time()
        self.fig = None
        self.canvas = None
        self.animation = None

        self.sensor_scale = None
        self.water_scale = None
        self.water_level_title = None
        self.profile_setup()

    def profile_setup(self):
        """
        profile_setup fills in the profile frame with
        sensor, actuator and suggestion frames. The sensor
        and actuator scales, graphs and labels should update
        in regular time intervals. It also adds home button
        to label_frame for user to navigate back to option page.
        """
        self.label.config(text=self.profile.title)

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

        # sensor_frame set up

        self.profile_frame.grid_columnconfigure(0, weight=3)
        self.profile_frame.grid_columnconfigure(1, weight=1)

        for n in range(3):
            self.profile_frame.grid_rowconfigure(n, weight=1)

        self.sensor_frame = Frame(
            self.profile_frame, bg=Constants.BACKGROUND.value
        )

        sensor_title = Label(
            self.sensor_frame, text=self.profile.sensor_frame_title
        )

        sensor_title.config(
            background=Constants.BACKGROUND.value,
            font=(Constants.FONT_STYLE.value, 15),
        )
        sensor_title.pack()

        self.curr_sensor_value_label = Label(
            self.sensor_frame, text=self.profile.sensor_value_description
        )
        self.curr_sensor_value_label.config(
            background=Constants.BACKGROUND.value,
            font=(Constants.FONT_STYLE.value, 15),
        )
        self.curr_sensor_value_label.pack()

        # scale_frame set up

        self.sensor_scale = SensorValueScale(self.profile, self.sensor_frame)

        self.graph_display()

        self.sensor_frame.grid(
            row=0,
            column=0,
            sticky="news",
            pady=Constants.EXTRA_PADDING.value,
            padx=Constants.EXTRA_PADDING.value,
            rowspan=3,
        )

        # actuator_frame set up

        self.general_actuation_setup()

        # suggestion_frame set up

        self.suggestion_frame = Frame(
            self.profile_frame, bg=Constants.BACKGROUND.value
        )
        suggestion_label = Label(self.suggestion_frame, text="Suggestion")
        suggestion_label.config(
            background=Constants.BACKGROUND.value,
            font=(Constants.FONT_STYLE.value, Constants.FONT_SIZE.value),
        )
        suggestion_label.pack()

        
        message_frame = Frame(self.suggestion_frame, height=400)
        self.msg = Label(message_frame, text=self.profile.suggestion)
        self.msg.pack()
        message_frame.pack()

        if not self.is_water:
            canvas= Canvas(message_frame, width= 150, height= 175)
        
            img = Image.open("assets/profilePagePlant.png")      
            new_img = ImageTk.PhotoImage(img.resize((150,150), Image.ANTIALIAS))
            canvas.create_image(0,25, anchor=NW, image=new_img)
            canvas.image = new_img
            canvas.pack()

        self.suggestion_frame.grid(
            row=2,
            column=1,
            sticky="news",
            pady=Constants.EXTRA_PADDING.value,
            padx=Constants.EXTRA_PADDING.value,
        )

        # Display on profile_frame

        self.profile_frame.pack(
            fill=BOTH,
            expand=True,
            pady=Constants.PADDING.value,
            padx=Constants.PADDING.value,
        )

    def get_xlabels(self, xar: List[float], no_xticks):
        """
        get_xlabels gets a list of x
        labels for x ticks of graph.

        :param xar: List of x values for graph.
        :type xar: list(float)
        :param no_xticks: Number of ticks displayed on graph x axis.
        :type no_xticks: int
        """
        if len(xar) > 0:
            range_seconds = (max(xar) - min(xar)).total_seconds()
            interval = range_seconds / (no_xticks - 1)
            curr = min(xar)
            locs = [curr]
            labels = [curr.strftime("%H:%M:%S")]
            for n in range(no_xticks - 1):
                curr = curr + timedelta(seconds=interval)
                locs.append(curr)
                labels.append(curr.strftime("%H:%M:%S"))
            return (locs, labels)
        else:
            return ([], [])

    def graph_display(self):
        """
        graph_display displays graph of sensor value
        over time with animated value updates.
        """
        graph_frame = Frame(self.sensor_frame, bg=Constants.BACKGROUND.value)
        y_label = self.profile.title + " (" + self.profile.unit + ")"
        xar = self.profile.time_list[-ProfilePage.NUM_OF_DATA:]
        yar = self.profile.val_list[-ProfilePage.NUM_OF_DATA:]

        self.fig = plt.figure(figsize=(5, 4), dpi=100, tight_layout=True)
        self.axs = self.fig.add_subplot(111)
        self.axs.plot(xar, yar)
        self.axs.set_xticks(self.get_xlabels(xar, ProfilePage.NO_XTICKS)[0])
        self.axs.set_xticklabels(
            self.get_xlabels(xar, ProfilePage.NO_XTICKS)[1]
        )
        self.canvas = FigureCanvasTkAgg(self.fig, graph_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(pady=15, padx=15)
        self.animation = FuncAnimation(
            self.fig, self.animate, interval=Constants.TIME_INTERVAL.value
        )
        self.axs.set(
            xlabel="Time (HH:MM:SS)",
            ylabel=y_label,
            title=self.profile.graph_title,
        )

        graph_frame.pack()

    def animate(self, i: int):
        """
        animate is the method called by FuncAnimation
        constantly update graph every time interval.
        This function also updates live displayed sensor
        and actuator values as well.

        :param i: Frame counter.
        :type i: int
        """
        if (
            time.time() - self.time_since_update
            >= Constants.TIME_INTERVAL.value
        ):
            self.profile.update_from_db(self.profile.title)
            self.curr_sensor_value_label.config(
                text=self.profile.sensor_value_description
            )
            self.sensor_scale.update(self.profile.sensor_value)
            if self.is_water:
                water_level = self.get_water_level()
                self.water_scale.update(water_level)
                self.water_level_title.config(
                    text="Water Level: " + str(water_level) + "%"
                )
            self.curr_actuator_value_label.config(
                text=self.profile.actuator_value_description
            )
            self.msg.config(text=self.profile.suggestion)
            self.time_since_update = time.time()
        if len(self.profile.time_list) < ProfilePage.NUM_OF_DATA:
            xar = self.profile.time_list
            yar = self.profile.val_list
        else:
            xar = self.profile.time_list[-ProfilePage.NUM_OF_DATA:]
            yar = self.profile.val_list[-ProfilePage.NUM_OF_DATA:]

        self.axs.clear()
        self.axs.plot(xar, yar)
        self.axs.set_xticks(self.get_xlabels(xar, ProfilePage.NO_XTICKS)[0])
        self.axs.set_xticklabels(
            self.get_xlabels(xar, ProfilePage.NO_XTICKS)[1]
        )
        self.axs.set(
            xlabel="Time (HH:MM:SS)",
            ylabel=self.profile.title + " (" + self.profile.unit + ")",
            title=self.profile.graph_title,
        )

    def home_button_action(self, binst: Button):
        """
        home_button_action allows the user to navigate back to option
        page by changing the title label and swapping profile_frame
        back to option_frame.

        :param binst: The home button itself.
        :type binst: Button
        """
        self.is_water = False
        self.animation.event_source.stop()
        self.profile_frame.pack_forget()
        self.option_frame.pack(
            expand=True,
            fill=BOTH,
            pady=Constants.PADDING.value,
            padx=Constants.PADDING.value,
        )
        binst.destroy()
        self.label.config(text="IoT FarmBeats")

    def general_actuation_setup(self):
        """
        general_actuation_setup fills in the actuation
        with a label showing current actuation value which
        updates in regular intervals. It also sets up an extra
        water level frame if the selected subsystem is Soil Moisture.
        """
        if self.is_water:
            y_padding = 0
        else: 
            y_padding = Constants.PADDING.value

        self.actuator_frame = Frame(
            self.profile_frame, bg=Constants.BACKGROUND.value
        )
        self.actuator_frame.grid_columnconfigure(0, weight=1)
        for n in range(3):
            self.actuator_frame.grid_rowconfigure(n, weight=1)

        actuatorTitle = Label(
            self.actuator_frame, text=self.profile.actuator_frame_title
        )

        actuatorTitle.config(
            background=Constants.BACKGROUND.value,
            font=(Constants.FONT_STYLE.value, Constants.FONT_SIZE.value),
        )

        actuatorTitle.grid(
            row=0, column=0, sticky="news", padx=Constants.PADDING.value, pady=y_padding,
        )

        mode_switch_frame = Frame(
            self.actuator_frame, bg=Constants.BACKGROUND.value
        )
        manual_mode = Label(mode_switch_frame, text="Manual")
        manual_mode.config(
            background="#CEE5DB",
            font=(Constants.FONT_STYLE.value, Constants.FONT_SIZE.value),
        )
        manual_mode.pack(side=RIGHT, padx=55)
        automatic_mode = Button(mode_switch_frame, text="Automatic")
        automatic_mode.config(
            background=Constants.BACKGROUND.value,
            font=(Constants.FONT_STYLE.value, Constants.FONT_SIZE.value),
        )
        automatic_mode.pack(side=RIGHT)

        mode_switch_frame.grid(
            row=1, column=0, sticky="news", padx=Constants.PADDING.value, pady=y_padding,
        )

        self.curr_actuator_value_label = Label(
            self.actuator_frame, text=self.profile.actuator_value_description
        )

        self.curr_actuator_value_label.config(
            background=Constants.BACKGROUND.value,
            font=(Constants.FONT_STYLE.value, Constants.FONT_SIZE.value),
        )

        self.curr_actuator_value_label.grid(
            row=2, column=0, sticky="news", padx=Constants.PADDING.value, pady=y_padding,
        )

        if self.is_water:
            self.actuator_frame.grid(
                row=0,
                column=1,
                sticky="news",
                pady=Constants.EXTRA_PADDING.value,
                padx=Constants.EXTRA_PADDING.value,
            )
            self.water_level_frame_setup()
        else:
            self.actuator_frame.grid(
                row=0,
                column=1,
                sticky="news",
                pady=Constants.EXTRA_PADDING.value,
                padx=Constants.EXTRA_PADDING.value,
                rowspan=2,
            )

    def get_water_level(self):
        """
        get_water_level gets water level from current profile,
        ensuring the value is between 0 and 100.

        :return: Current water level.
        :rtype: Int
        """
        if self.profile.water_level_value:
            if self.profile.water_level_value > 100:
                return 100
            elif self.profile.water_level_value < 0:
                return 0
            else:
                return self.profile.water_level_value
        else:
            return 0

    def water_level_frame_setup(self):
        """
        water_level_frame_setup sets up the extra water
        level frame for the water level subsystem
        """

        water_level_frame = Frame(
            self.profile_frame, bg=Constants.BACKGROUND.value
        )
        water_level_frame.grid_columnconfigure(0, weight=1)
        water_level_frame.grid_rowconfigure(0, weight=1)
        water_level_frame.grid_rowconfigure(1, weight=3)
        water_level_frame.grid_rowconfigure(2, weight=1)

        water_level = self.get_water_level()

        self.water_level_title = Label(
            water_level_frame,
            text="Water Level: " + str(water_level) + "%",
        )

        self.water_level_title.config(
            background=Constants.BACKGROUND.value,
            font=(Constants.FONT_STYLE.value, Constants.FONT_SIZE.value),
        )

        self.water_level_title.grid(
            row=0, column=0, sticky="news", padx=Constants.PADDING.value
        )

        self.water_scale = WaterScale(water_level_frame, water_level)

        self.water_level_title.config(
            background=Constants.BACKGROUND.value,
            font=(Constants.FONT_STYLE.value, Constants.FONT_SIZE.value),
        )

        self.water_level_title.grid(
            row=0, column=0, sticky="news", padx=Constants.PADDING.value
        )

        water_level_frame.grid(
            row=1,
            column=1,
            sticky="news",
            padx=Constants.PADDING.value,
        )
