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

    def profile_setup(self, profile_name):

        profile = ProfileInformation(profile_name)
        self.label.config(text=profile.title)
        img = Image.open("assets/homeIcon.png")
        home_icon = ImageTk.PhotoImage(img)

        home_button = Button(self.label_frame, image=home_icon, borderwidth=0)
        home_button.image = home_icon

        home_button[
            "command"
        ] = lambda idx="Home", \
            binst=home_button: self.home_button_action(binst)

        home_button.pack()
        home_button.place(bordermode=INSIDE, x=5, y=5)

        for n in range(2):
            self.profile_frame.grid_columnconfigure(n, weight=1)
        for n in range(4):
            self.profile_frame.grid_rowconfigure(n, weight=1)

        # sensor_frame set up

        sensor_frame = Frame(self.profile_frame, bg=BACKGROUND)

        sensor_title = Label(sensor_frame, text=profile.sensor_frame_title)
        sensor_title.config(background=BACKGROUND, font=("Courier", 15))
        sensor_title.pack()

        value = Label(sensor_frame, text=profile.sensor_value_description)
        value.config(background=BACKGROUND)
        value.config(font=("Courier", 15))
        value.pack()

        # scale_frame set up

        scale_frame = Frame(sensor_frame, bg=BACKGROUND)
        offset = 25
        range_ = profile.bound[1] - profile.bound[0]
        l1 = (((profile.extr[0] - profile.bound[0]) / range_) * 400) + offset
        l2 = (((profile.extr[1] - profile.bound[0]) / range_) * 400) + offset
        l3 = (((profile.extr[2] - profile.bound[0]) / range_) * 400) + offset
        l4 = (((profile.extr[3] - profile.bound[0]) / range_) * 400) + offset

        line = ((profile.sensor_value - profile.bound[0]) / range_) * 400
        scale_canvas = tkinter.Canvas(scale_frame, height=50, width=400+2*offset)

        scale_canvas.create_rectangle(0 + offset, 0, l1, 30, fill=RED, width=0)
        scale_canvas.create_rectangle(l1, 0, l2, 30, fill=AMBER, width=0)
        scale_canvas.create_rectangle(l2, 0, l3, 30, fill=GREEN, width=0)
        scale_canvas.create_rectangle(l3, 0, l4, 30, fill=AMBER, width=0)
        scale_canvas.create_rectangle(l4, 0, 400+ offset, 30, fill=RED, width=0)
        scale_canvas.create_line(offset, 15, line+offset, 15, width=3)
        scale_canvas.create_text(offset, 35, text=str(profile.bound[0]), fill="black", font=('Courier'))
        scale_canvas.create_text(l1, 45, text=str(profile.extr[0]), fill="black", font=('Courier'))
        scale_canvas.create_line(l1-1, 30, l1-1, 40, fill='grey')
        scale_canvas.create_text(l2, 35, text=str(profile.extr[1]), fill="black", font=('Courier'))
        scale_canvas.create_text(l3, 45, text=str(profile.extr[2]), fill="black", font=('Courier'))
        scale_canvas.create_line(l3-1, 30, l3-1, 40, fill='grey')
        scale_canvas.create_text(l4, 35, text=str(profile.extr[3]), fill="black", font=('Courier'))
        scale_canvas.create_text(400+offset, 45, text=str(profile.bound[1]), fill="black", font=('Courier'))
        scale_canvas.create_line(400+offset-1, 30, 400+offset-1, 40, fill='grey')

        scale_canvas.pack()
        scale_frame.pack()
        
        self.graph_display(sensor_frame, profile)
        sensor_frame.grid(
            row=0,
            column=0,
            sticky="news",
            pady=PADDING,
            padx=PADDING,
            rowspan=4,
        )

        # actuator_frame set up

        actuator_frame = Frame(self.profile_frame, bg=BACKGROUND)
        actuator_frame.grid_columnconfigure(0, weight=1)
        for n in range(3):
            actuator_frame.grid_rowconfigure(n, weight=1)

        actuatorTitle = Label(
            actuator_frame,
            text=profile.actuator_frame_title
        )

        actuatorTitle.config(background=BACKGROUND, font=("Courier", 15))

        actuatorTitle.grid(
            row=0, column=0, sticky="news", pady=PADDING, padx=PADDING
        )

        mode_switch_frame = Frame(actuator_frame, bg=BACKGROUND)
        manual_mode = Label(mode_switch_frame, text="Manual")
        manual_mode.config(background="#CEE5DB", font=("Courier", 15))
        manual_mode.pack(side=RIGHT)
        automatic_mode = Button(mode_switch_frame, text="Automatic")
        automatic_mode.config(background=BACKGROUND, font=("Courier", 15))
        automatic_mode.pack(side=LEFT)

        mode_switch_frame.grid(
            row=1, column=0, sticky="news", pady=PADDING, padx=PADDING
        )

        actuator_val = Label(
            actuator_frame, text=profile.actuator_value_description
        )

        actuator_val.config(background=BACKGROUND, font=("Courier", 15))

        actuator_val.grid(
            row=2, column=0, sticky="news", pady=PADDING, padx=PADDING
        )

        actuator_frame.grid(
            row=0,
            column=1,
            sticky="news",
            pady=PADDING,
            padx=PADDING,
            rowspan=3,
        )

        # suggestion_frame set up

        suggestion_frame = Frame(self.profile_frame, bg=BACKGROUND)
        suggestion_label = Label(suggestion_frame, text="Suggestion")
        suggestion_label.config(background=BACKGROUND, font=("Courier", 15))
        suggestion_label.pack()
        message_frame = Frame(suggestion_frame, bg="#FFFFFF", height=400)
        msg = Label(message_frame, text=profile.suggestion)
        msg.pack()
        message_frame.pack()

        suggestion_frame.grid(
            row=3, column=1, sticky="news", pady=PADDING, padx=PADDING
        )

        # Display on profile_frame

        self.profile_frame.pack(fill=BOTH, expand=True, pady=15, padx=15)

    def graph_display(self, frame, profile):

        y_label = profile.title + " (" + profile.unit + ")"

        data_frame = DataFrame(
            {"Time (ms)": profile.time_list, y_label: profile.val_list},
            columns=["Time (ms)", y_label],
        )

        fig = plt.Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        FigureCanvasTkAgg(fig, frame).get_tk_widget().pack(pady=15, padx=15)
        data_frame = (
            data_frame[["Time (ms)", y_label]].groupby("Time (ms)").sum()
        )

        data_frame.plot(
            linewidth=0.5,
            kind="line",
            legend=True,
            ax=ax,
            color="r",
            fontsize=10,
        )

        ax.set(xlabel="Time (ms)", ylabel=y_label, title=profile.graph_title)

    def home_button_action(self, binst):
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
        self.option_frame.pack_forget()
        self.profile_setup("Water")

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
