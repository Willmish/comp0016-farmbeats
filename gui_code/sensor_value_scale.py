from tkinter import Frame
import tkinter
import globals
from profileInformation import ProfileInformation


class SensorValueScale:
    def __init__(self, profile: ProfileInformation, parent_frame: Frame):
        scale_frame = Frame(parent_frame, bg=globals.background)
        offset = 25
        range_ = profile.bound[1] - profile.bound[0]
        l1 = (((profile.extr[0] - profile.bound[0])
              / range_) * 400) + offset
        l2 = (((profile.extr[1] - profile.bound[0])
              / range_) * 400) + offset
        l3 = (((profile.extr[2] - profile.bound[0])
              / range_) * 400) + offset
        l4 = (((profile.extr[3] - profile.bound[0])
              / range_) * 400) + offset

        if profile.sensor_value:
            line = ((profile.sensor_value - profile.bound[0])
                    / range_) * 400
        else:
            line = 0

        scale_canvas = tkinter.Canvas(
            scale_frame,
            height=50,
            width=400 + 2 * offset,
            background=globals.background,
            highlightthickness=0,
        )

        scale_canvas.create_rectangle(
            0 + offset, 0, l1, 30,
            fill=globals.red, width=0
        )
        scale_canvas.create_rectangle(
            l1, 0, l2, 30,
            fill=globals.amber, width=0
        )
        scale_canvas.create_rectangle(
            l2, 0, l3, 30,
            fill=globals.green, width=0
        )
        scale_canvas.create_rectangle(
            l3, 0, l4, 30,
            fill=globals.amber, width=0
        )
        scale_canvas.create_rectangle(
            l4, 0, 400 + offset, 30,
            fill=globals.red, width=0
        )
        scale_canvas.create_line(
            offset, 15, line + offset, 15, width=3
        )
        scale_canvas.create_text(
            offset, 35, text=str(profile.bound[0]),
            fill="black", font=("Courier")
        )
        scale_canvas.create_text(
            l1, 45, text=str(profile.extr[0]),
            fill="black", font=("Courier")
        )
        scale_canvas.create_line(
            l1 - 1, 30, l1 - 1, 40, fill="grey"
        )
        scale_canvas.create_text(
            l2, 35, text=str(profile.extr[1]),
            fill="black", font=("Courier")
        )
        scale_canvas.create_text(
            l3, 45, text=str(profile.extr[2]),
            fill="black", font=("Courier")
        )
        scale_canvas.create_line(
            l3 - 1, 30, l3 - 1, 40, fill="grey"
        )
        scale_canvas.create_text(
            l4, 35, text=str(profile.extr[3]),
            fill="black", font=("Courier")
        )
        scale_canvas.create_text(
            400 + offset,
            45,
            text=str(profile.bound[1]),
            fill="black",
            font=("Courier"),
        )
        scale_canvas.create_line(
            400 + offset - 1, 30,
            400 + offset - 1, 40,
            fill="grey"
        )

        scale_canvas.pack()
        scale_frame.pack()
