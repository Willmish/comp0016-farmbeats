from tkinter import Frame
import tkinter
from tools.constants import Constants
from profile_view.profile_information import ProfileInformation


class SensorValueScale:
    def __init__(self, profile: ProfileInformation, parent_frame: Frame):
        self.profile = profile
        self.scale_frame = Frame(parent_frame, bg=Constants.BACKGROUND.value)
        self.offset = 25
        self.range_ = profile.bound[1] - profile.bound[0]
        l1 = (((profile.extr[0] - profile.bound[0])
              / self.range_) * 400) + self.offset
        l2 = (((profile.extr[1] - profile.bound[0])
              / self.range_) * 400) + self.offset
        l3 = (((profile.extr[2] - profile.bound[0])
              / self.range_) * 400) + self.offset
        l4 = (((profile.extr[3] - profile.bound[0])
              / self.range_) * 400) + self.offset

        if profile.sensor_value:
            line = ((profile.sensor_value - profile.bound[0])
                    / self.range_) * 400
        else:
            line = 0

        self.scale_canvas = tkinter.Canvas(
            self.scale_frame,
            height=50,
            width=400 + 2 * self.offset,
            background=Constants.BACKGROUND.value,
            highlightthickness=0,
        )

        self.scale_canvas.create_rectangle(
            0 + self.offset, 0, l1, 30,
            fill=Constants.RED_RGB.value, width=0
        )
        self.scale_canvas.create_rectangle(
            l1, 0, l2, 30,
            fill=Constants.AMBER_RGB.value, width=0
        )
        self.scale_canvas.create_rectangle(
            l2, 0, l3, 30,
            fill=Constants.GREEN_RGB.value, width=0
        )
        self.scale_canvas.create_rectangle(
            l3, 0, l4, 30,
            fill=Constants.AMBER_RGB.value, width=0
        )
        self.scale_canvas.create_rectangle(
            l4, 0, 400 + self.offset, 30,
            fill=Constants.RED_RGB.value, width=0
        )
        self.line = self.scale_canvas.create_line(
            self.offset, 15, line + self.offset, 15, width=3
        )
        self.scale_canvas.create_text(
            self.offset, 35, text=str(profile.bound[0]),
            fill="black", font=("Courier")
        )
        self.scale_canvas.create_text(
            l1, 45, text=str(profile.extr[0]),
            fill="black", font=("Courier")
        )
        self.scale_canvas.create_line(
            l1 - 1, 30, l1 - 1, 40, fill="grey"
        )
        self.scale_canvas.create_text(
            l2, 35, text=str(profile.extr[1]),
            fill="black", font=("Courier")
        )
        self.scale_canvas.create_text(
            l3, 45, text=str(profile.extr[2]),
            fill="black", font=("Courier")
        )
        self.scale_canvas.create_line(
            l3 - 1, 30, l3 - 1, 40, fill="grey"
        )
        self.scale_canvas.create_text(
            l4, 35, text=str(profile.extr[3]),
            fill="black", font=("Courier")
        )
        self.scale_canvas.create_text(
            400 + self.offset,
            45,
            text=str(profile.bound[1]),
            fill="black",
            font=("Courier"),
        )
        self.scale_canvas.create_line(
            400 + self.offset - 1, 30,
            400 + self.offset - 1, 40,
            fill="grey"
        )

        self.scale_canvas.pack()
        self.scale_frame.pack()
    
    def update(self, new_value):
        self.scale_canvas.delete(self.line)
        line = ((new_value - self.profile.bound[0])
                    / self.range_) * 400
        self.line = self.scale_canvas.create_line(
            self.offset, 15, line + self.offset, 15, width=3
        )
        


