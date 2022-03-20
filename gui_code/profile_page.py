from datetime import timedelta
from tkinter import Frame, Label, Button, INSIDE, BOTH, RIGHT, LEFT
import tkinter
import matplotlib.pyplot as plt
from sensor_value_scale import SensorValueScale
from profile_information import ProfileInformation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image
from PIL import ImageTk
from matplotlib.animation import FuncAnimation
import time
from constants import Constants


class ProfilePage:
    def __init__(
        self, profile_name, profile_frame, title_frame, label, option_frame
    ):
        self.profile = ProfileInformation(profile_name)
        self.option_frame = option_frame
        self.profile_frame = profile_frame
        self.label_frame = title_frame
        self.label = label

        self.sensor_frame = None
        self.curr_sensor_value_label = None
        self.curr_actuator_value_label = None
        self.actuator_frame = None
        self.suggestion_frame = None

        self.water_level_frame = None
        self.is_water = False

        # for graph display
        self.graph_frame = None
        self.current_profile = None
        self.time_since_update = time.time()
        self.fig = None
        self.plot = None
        self.data_plot = None
        self.canvas = None
        self.animation = None
        self.no_xticks = 4
        self.profile_setup()

    def profile_setup(self):
        self.label.config(text=self.profile.title)

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
            self.profile_frame.grid_columnconfigure(n, weight=1)
        for n in range(3):
            self.profile_frame.grid_rowconfigure(n, weight=1)

        self.sensor_frame = Frame(self.profile_frame, bg=Constants.BACKGROUND)

        sensor_title = Label(
            self.sensor_frame, text=self.profile.sensor_frame_title
        )

        sensor_title.config(
            background=Constants.BACKGROUND, font=("Courier", 15)
        )
        sensor_title.pack()

        self.curr_sensor_value_label = Label(
            self.sensor_frame, text=self.profile.sensor_value_description
        )
        self.curr_sensor_value_label.config(
            background=Constants.BACKGROUND, font=("Courier", 15)
        )
        self.curr_sensor_value_label.pack()

        # scale_frame set up

        SensorValueScale(self.profile, self.sensor_frame)

        self.graph_display()

        self.sensor_frame.grid(
            row=0,
            column=0,
            sticky="news",
            pady=Constants.PADDING,
            padx=Constants.PADDING,
            rowspan=3,
        )

        # actuator_frame set up

        self.general_actuation_setup()

        # suggestion_frame set up

        self.suggestion_frame = Frame(
            self.profile_frame, bg=Constants.BACKGROUND
        )
        suggestion_label = Label(self.suggestion_frame, text="Suggestion")
        suggestion_label.config(
            background=Constants.BACKGROUND, font=("Courier", 15)
        )
        suggestion_label.pack()
        message_frame = Frame(self.suggestion_frame, bg="#FFFFFF", height=400)
        msg = Label(message_frame, text=self.profile.suggestion)
        msg.pack()
        message_frame.pack()

        self.suggestion_frame.grid(
            row=2,
            column=1,
            sticky="news",
            pady=Constants.PADDING,
            padx=Constants.PADDING,
        )

        # Display on profile_frame

        self.profile_frame.pack(fill=BOTH, expand=True, pady=15, padx=15)

    def get_xlabels(self, xar, no_xticks):
        range_seconds = (max(xar) - min(xar)).total_seconds()
        interval = range_seconds / (no_xticks - 1)
        curr = min(xar)
        labels = [curr]
        for n in range(no_xticks - 1):
            curr = curr + timedelta(seconds=interval)
            labels.append(curr)
        return labels

    def graph_display(self):
        self.graph_frame = Frame(self.sensor_frame, bg=Constants.BACKGROUND)
        y_label = self.profile.title + " (" + self.profile.unit + ")"
        xar = self.profile.time_list[-100:]
        yar = self.profile.val_list[-100:]

        self.fig = plt.figure(figsize=(5, 4), dpi=100, tight_layout=True)
        self.axs = self.fig.add_subplot(111)
        self.axs.plot(xar, yar)
        self.axs.set_xticks(self.get_xlabels(xar, self.no_xticks))
        self.canvas = FigureCanvasTkAgg(self.fig, self.graph_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(pady=15, padx=15)
        self.animation = FuncAnimation(
            self.fig, self.animate, interval=Constants.TIME_INTERVAL
        )
        self.axs.set(
            xlabel="Time (ms)", ylabel=y_label, title=self.profile.graph_title
        )

        self.graph_frame.pack()

    def animate(self, i):
        if time.time() - self.time_since_update >= Constants.TIME_INTERVAL:
            self.profile.update_from_db(self.profile.title)
            self.curr_sensor_value_label.config(
                text=self.profile.sensor_value_description
            )
            self.curr_actuator_value_label.config(
                text=self.profile.actuator_value_description
            )
            print(self.profile.sensor_value_description)
            print(self.profile.actuator_value_description)
            print("time: " + str(self.profile.time_list[-1]))
            self.time_since_update = time.time()

        if len(self.profile.time_list) < 100:
            xar = self.profile.time_list
            yar = self.profile.val_list
        else:
            xar = self.profile.time_list[-100:]
            yar = self.profile.val_list[-100:]

        self.axs.clear()
        self.axs.plot(xar, yar)
        self.axs.set_xticks(self.get_xlabels(xar, self.no_xticks))
        self.axs.set(
            xlabel="Time (ms)",
            ylabel=self.profile.title + " (" + self.profile.unit + ")",
            title=self.profile.graph_title,
        )

    def home_button_action(self, binst):
        self.is_water = False
        self.animation.event_source.stop()
        self.profile_frame.pack_forget()
        self.option_frame.pack(expand=True, fill=BOTH, pady=15, padx=15)
        binst.destroy()
        self.label.config(text="IoT FarmBeats")

    def general_actuation_setup(self):

        self.actuator_frame = Frame(
            self.profile_frame, bg=Constants.BACKGROUND
        )
        self.actuator_frame.grid_columnconfigure(0, weight=1)
        for n in range(3):
            self.actuator_frame.grid_rowconfigure(n, weight=1)

        actuatorTitle = Label(
            self.actuator_frame, text=self.profile.actuator_frame_title
        )

        actuatorTitle.config(
            background=Constants.BACKGROUND, font=("Courier", 15)
        )

        actuatorTitle.grid(
            row=0, column=0, sticky="news", padx=Constants.PADDING
        )

        mode_switch_frame = Frame(self.actuator_frame, bg=Constants.BACKGROUND)
        manual_mode = Label(mode_switch_frame, text="Manual")
        manual_mode.config(background="#CEE5DB", font=("Courier", 15))
        manual_mode.pack(side=RIGHT)
        automatic_mode = Button(mode_switch_frame, text="Automatic")
        automatic_mode.config(
            background=Constants.BACKGROUND, font=("Courier", 15)
        )
        automatic_mode.pack(side=LEFT)

        mode_switch_frame.grid(
            row=1, column=0, sticky="news", padx=Constants.PADDING
        )

        self.curr_actuator_value_label = Label(
            self.actuator_frame, text=self.profile.actuator_value_description
        )

        self.curr_actuator_value_label.config(
            background=Constants.BACKGROUND, font=("Courier", 15)
        )

        self.curr_actuator_value_label.grid(
            row=2, column=0, sticky="news", padx=Constants.PADDING
        )

        if self.is_water:
            self.actuator_frame.grid(
                row=0,
                column=1,
                sticky="news",
                pady=Constants.PADDING,
                padx=Constants.PADDING,
            )
            self.water_level_frame_setup()
        else:
            self.actuator_frame.grid(
                row=0,
                column=1,
                sticky="news",
                pady=Constants.PADDING,
                padx=Constants.PADDING,
                rowspan=2,
            )

    def water_level_frame_setup(self):

        water_level_value = 50  # dummy data for now

        self.water_level_frame = Frame(
            self.profile_frame, bg=Constants.BACKGROUND
        )
        self.water_level_frame.grid_columnconfigure(0, weight=1)
        self.water_level_frame.grid_rowconfigure(0, weight=1)
        self.water_level_frame.grid_rowconfigure(1, weight=3)
        self.water_level_frame.grid_rowconfigure(2, weight=1)

        water_level_title = Label(
            self.water_level_frame,
            text="Water Level: " + str(water_level_value) + "%",
        )

        water_level_title.config(
            background=Constants.BACKGROUND, font=("Courier", 15)
        )

        water_level_title.grid(
            row=0, column=0, sticky="news", padx=Constants.PADDING
        )

        scale_frame = Frame(self.water_level_frame)

        h = 200
        y_offset = 20
        x_offset = 10

        scale_canvas = tkinter.Canvas(
            scale_frame,
            height=h + y_offset,
            width=80 + (2 * x_offset),
        )

        length = (water_level_value / 100) * h

        scale_canvas.create_rectangle(
            x_offset, y_offset, 50 + x_offset, h + y_offset, width=0
        )
        scale_canvas.create_rectangle(
            x_offset,
            h + y_offset,
            50 + x_offset,
            h - length + y_offset,
            fill="#B7DEF2",
            width=0,
        )
        scale_canvas.create_line(
            x_offset, h + y_offset, x_offset, y_offset, fill="#000000", width=3
        )
        scale_canvas.create_line(
            49 + x_offset,
            h + y_offset,
            49 + x_offset,
            y_offset,
            fill="#000000",
            width=3,
        )
        scale_canvas.create_line(
            50 + x_offset,
            h + y_offset,
            x_offset,
            h + y_offset,
            fill="#000000",
            width=3,
        )
        scale_canvas.create_text(
            50 + (2 * x_offset) + 10,
            y_offset,
            text="100%",
            fill="black",
            font=("Courier"),
        )
        scale_canvas.create_text(
            50 + (2 * x_offset) + 10,
            h // 2 + y_offset - 5,
            text="50%",
            fill="black",
            font=("Courier"),
        )
        scale_canvas.create_text(
            50 + (2 * x_offset) + 10,
            h + y_offset - 5,
            text="0%",
            fill="black",
            font=("Courier"),
        )

        scale_canvas.pack()
        scale_frame.grid(
            row=1,
            column=0,
            sticky="news",
            padx=Constants.PADDING,
        )

        water_level_title.config(
            background=Constants.BACKGROUND, font=("Courier", 15)
        )

        water_level_title.grid(
            row=0, column=0, sticky="news", padx=Constants.PADDING
        )

        self.water_level_frame.grid(
            row=1,
            column=1,
            sticky="news",
            pady=Constants.PADDING,
            padx=Constants.PADDING,
        )
