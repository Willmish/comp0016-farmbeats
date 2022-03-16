from tkinter import Frame, Label, Button, INSIDE, BOTH, RIGHT, LEFT, Tk
import tkinter
import matplotlib.pyplot as plt
from sensor_value_scale import SensorValueScale
from profileInformation import ProfileInformation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image
from PIL import ImageTk
from matplotlib.animation import FuncAnimation
from matplotlib import style
import time

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
        self.widget = None
        self.animation = None

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
            row=0, column=0, sticky="news",
            pady=PADDING, padx=PADDING
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
            row=0, column=1, sticky="news",
            pady=PADDING, padx=PADDING
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
            row=1, column=0, sticky="news",
            pady=PADDING, padx=PADDING
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
            row=1, column=1, sticky="news",
            pady=PADDING, padx=PADDING
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
            row=1, column=2, sticky="news",
            pady=PADDING, padx=PADDING
        )

        self.option_frame.pack(expand=True, fill=BOTH, pady=15, padx=15)

    def general_actuation_setup(self):

        self.actuator_frame = Frame(self.profile_frame, bg=BACKGROUND)
        self.actuator_frame.grid_columnconfigure(0, weight=1)
        for n in range(3):
            self.actuator_frame.grid_rowconfigure(n, weight=1)

        actuatorTitle = Label(
            self.actuator_frame,
            text=self.profile.actuator_frame_title
        )

        actuatorTitle.config(background=BACKGROUND, font=("Courier", 15))

        actuatorTitle.grid(row=0, column=0, sticky="news", padx=PADDING)

        mode_switch_frame = Frame(self.actuator_frame, bg=BACKGROUND)
        manual_mode = Label(mode_switch_frame, text="Manual")
        manual_mode.config(background="#CEE5DB", font=("Courier", 15))
        manual_mode.pack(side=RIGHT)
        automatic_mode = Button(mode_switch_frame, text="Automatic")
        automatic_mode.config(background=BACKGROUND, font=("Courier", 15))
        automatic_mode.pack(side=LEFT)

        mode_switch_frame.grid(row=1, column=0, sticky="news", padx=PADDING)

        self.curr_actuator_value_label = Label(
            self.actuator_frame, text=self.profile.actuator_value_description
        )

        self.curr_actuator_value_label.config(
            background=BACKGROUND, font=("Courier", 15)
        )

        self.curr_actuator_value_label.grid(
            row=2, column=0, sticky="news", padx=PADDING
        )

        if self.is_water:
            self.actuator_frame.grid(
                row=0,
                column=1,
                sticky="news",
                pady=PADDING,
                padx=PADDING,
            )
            self.water_level_frame_setup()
        else:
            self.actuator_frame.grid(
                row=0, column=1, sticky="news",
                pady=PADDING, padx=PADDING, rowspan=2
            )

    def water_level_frame_setup(self):

        water_level_value = 50  # dummy data for now

        self.water_level_frame = Frame(self.profile_frame, bg=BACKGROUND)
        self.water_level_frame.grid_columnconfigure(0, weight=1)
        self.water_level_frame.grid_rowconfigure(0, weight=1)
        self.water_level_frame.grid_rowconfigure(1, weight=3)
        self.water_level_frame.grid_rowconfigure(2, weight=1)

        water_level_title = Label(
            self.water_level_frame,
            text="Water Level: " + str(water_level_value) + "%"
        )

        water_level_title.config(background=BACKGROUND, font=("Courier", 15))

        water_level_title.grid(row=0, column=0, sticky="news", padx=PADDING)

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
            x_offset, h + y_offset, x_offset,
            y_offset, fill="#000000", width=3
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
            50 + x_offset, h + y_offset, x_offset,
            h + y_offset, fill="#000000", width=3
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
            padx=PADDING,
        )

        water_level_title.config(
            background=BACKGROUND, font=("Courier", 15)
        )

        water_level_title.grid(row=0, column=0, sticky="news", padx=PADDING)

        self.water_level_frame.grid(
            row=1,
            column=1,
            sticky="news",
            pady=PADDING,
            padx=PADDING,
        )

    def profile_setup(self, profile_name):
        self.profile = ProfileInformation(profile_name)
        self.label.config(text=self.profile.title)
        img = Image.open("assets/homeIcon.png")
        home_icon = ImageTk.PhotoImage(img)

        home_button = Button(
            self.label_frame, image=home_icon, borderwidth=0
        )
        home_button.image = home_icon

        home_button[
            "command"
        ] = lambda idx="Home", \
            binst=home_button: self.home_button_action(binst)

        home_button.pack()
        home_button.place(bordermode=INSIDE, x=5, y=5)

        for n in range(2):
            self.profile_frame.grid_columnconfigure(n, weight=1)
        for n in range(3):
            self.profile_frame.grid_rowconfigure(n, weight=1)

        self.sensor_frame = Frame(self.profile_frame, bg=BACKGROUND)

        sensor_title = Label(
            self.sensor_frame, text=self.profile.sensor_frame_title
        )

        sensor_title.config(background=BACKGROUND, font=("Courier", 15))
        sensor_title.pack()

        self.curr_sensor_value_label = Label(
            self.sensor_frame, text=self.profile.sensor_value_description
        )
        self.curr_sensor_value_label.config(
            background=BACKGROUND, font=("Courier", 15)
        )
        self.curr_sensor_value_label.pack()

        # scale_frame set up

        SensorValueScale(self.profile, self.sensor_frame)

        self.graph_display()

        self.sensor_frame.grid(
            row=0,
            column=0,
            sticky="news",
            pady=PADDING,
            padx=PADDING,
            rowspan=3,
        )

        # actuator_frame set up

        self.general_actuation_setup()

        # suggestion_frame set up

        self.suggestion_frame = Frame(self.profile_frame, bg=BACKGROUND)
        suggestion_label = Label(self.suggestion_frame, text="Suggestion")
        suggestion_label.config(background=BACKGROUND, font=("Courier", 15))
        suggestion_label.pack()
        message_frame = Frame(self.suggestion_frame, bg="#FFFFFF", height=400)
        msg = Label(message_frame, text=self.profile.suggestion)
        msg.pack()
        message_frame.pack()

        self.suggestion_frame.grid(
            row=2, column=1, sticky="news", pady=PADDING, padx=PADDING
        )

        # Display on profile_frame

        self.profile_frame.pack(fill=BOTH, expand=True, pady=15, padx=15)

    def graph_display(self):
        self.graph_frame = Frame(self.sensor_frame, bg=BACKGROUND)

        y_label = self.profile.title + " (" + self.profile.unit + ")"
        xar = self.profile.time_list[-100:]
        yar = self.profile.val_list[-100:]
        self.fig = plt.figure(figsize=(5, 4), dpi=100, tight_layout=True)

        self.axs = self.fig.add_subplot(111)
        self.axs.plot(xar, yar)

        # loc = dates.AutoDateLocator(minticks=4, maxticks=4)
        # self.fig.subplots().xaxis.set_major_locator(loc)
        # fmt = dates.AutoDateFormatter(loc)
        # self.fig.subplots().xaxis.set_major_formatter(fmt)

        self.canvas = FigureCanvasTkAgg(
            self.fig, self.graph_frame
        )

        self.canvas.draw()
        self.canvas.get_tk_widget().pack(pady=15, padx=15)
        self.animation = FuncAnimation(
            self.fig, self.animate, interval=TIME_INTERVAL
        )

        self.axs.set(
            xlabel="Time (ms)", ylabel=y_label,
            title=self.profile.graph_title
        )

        self.graph_frame.pack()

    def animate(self, i):
        if time.time() - self.time_since_update >= TIME_INTERVAL:
            self.profile.update_from_db(self.profile.title)
            self.curr_sensor_value_label.config(
                text=self.profile.sensor_value_description
            )
            self.curr_actuator_value_label.config(
                text=self.profile.actuator_value_description
            )
            self.time_since_update = time.time()

        if len(self.profile.time_list) < 100:
            xar = self.profile.time_list
            yar = self.profile.val_list
        else:
            xar = self.profile.time_list[-100:]
            yar = self.profile.val_list[-100:]

        self.axs.clear()
        self.axs.plot(xar, yar)
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

    def temp_button_action(self):
        self.option_frame.pack_forget()
        self.profile_setup("Temperature")

    def humidity_button_action(self):
        self.option_frame.pack_forget()
        self.profile_setup("Humidity")

    def brightness_button_action(self):
        self.option_frame.pack_forget()
        self.profile_setup("Brightness")

    def water_button_action(self):
        self.is_water = True
        self.option_frame.pack_forget()
        self.profile_setup("Water Level")

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
