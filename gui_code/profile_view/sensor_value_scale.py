from tkinter import Frame
import tkinter
from tools.constants import Constants
from profile_view.profile_information import ProfileInformation


class SensorValueScale:
    OFFSET = 25
    WIDTH = 400
    HEIGHT = 30
    TEXT_HEIGHT_1 = 35
    TEXT_HEIGHT_2 = 45
    MAIN_LINE_HEIGHT = 15
    MAIN_LINE_WIDTH = 3
    LABEL_LINE_LENGTH = 10
    LABEL_LINE_HEIGHT = 30

    def __init__(self, profile: ProfileInformation, parent_frame: Frame):
        """
        __init__ Displays sensor scale to show current sensor value and state.
        :param profile:
        :type profile: ProfileInformation
        :param parent_frame:
        :type parent_frame: Frame
        """
        self.profile = profile
        self.scale_frame = Frame(parent_frame, bg=Constants.BACKGROUND.value)
        self.range_ = profile.bound[1] - profile.bound[0]
        l1 = (
            ((profile.extr[0] - profile.bound[0]) / self.range_)
            * SensorValueScale.WIDTH
        ) + SensorValueScale.OFFSET
        l2 = (
            ((profile.extr[1] - profile.bound[0]) / self.range_)
            * SensorValueScale.WIDTH
        ) + SensorValueScale.OFFSET
        l3 = (
            ((profile.extr[2] - profile.bound[0]) / self.range_)
            * SensorValueScale.WIDTH
        ) + SensorValueScale.OFFSET
        l4 = (
            ((profile.extr[3] - profile.bound[0]) / self.range_)
            * SensorValueScale.WIDTH
        ) + SensorValueScale.OFFSET

        if profile.sensor_value:
            line = (
                (profile.sensor_value - profile.bound[0]) / self.range_
            ) * SensorValueScale.WIDTH
        else:
            line = 0

        self.scale_canvas = tkinter.Canvas(
            self.scale_frame,
            height=50,
            width=SensorValueScale.WIDTH + 2 * SensorValueScale.OFFSET,
            background=Constants.BACKGROUND.value,
            highlightthickness=0,
        )

        self.scale_canvas.create_rectangle(
            0 + SensorValueScale.OFFSET,
            0,
            l1,
            SensorValueScale.HEIGHT,
            fill=Constants.RED_RGB.value,
            width=0,
        )
        self.scale_canvas.create_rectangle(
            l1,
            0,
            l2,
            SensorValueScale.HEIGHT,
            fill=Constants.AMBER_RGB.value,
            width=0,
        )
        self.scale_canvas.create_rectangle(
            l2,
            0,
            l3,
            SensorValueScale.HEIGHT,
            fill=Constants.GREEN_RGB.value,
            width=0,
        )
        self.scale_canvas.create_rectangle(
            l3,
            0,
            l4,
            SensorValueScale.HEIGHT,
            fill=Constants.AMBER_RGB.value,
            width=0,
        )
        self.scale_canvas.create_rectangle(
            l4,
            0,
            SensorValueScale.WIDTH + SensorValueScale.OFFSET,
            SensorValueScale.HEIGHT,
            fill=Constants.RED_RGB.value,
            width=0,
        )
        self.line = self.scale_canvas.create_line(
            SensorValueScale.OFFSET,
            SensorValueScale.MAIN_LINE_HEIGHT,
            line + SensorValueScale.OFFSET,
            SensorValueScale.MAIN_LINE_HEIGHT,
            width=SensorValueScale.MAIN_LINE_WIDTH,
        )
        self.scale_canvas.create_text(
            SensorValueScale.OFFSET,
            SensorValueScale.TEXT_HEIGHT_1,
            text=str(profile.bound[0]),
            fill="black",
            font=(Constants.FONT_STYLE.value),
        )
        self.scale_canvas.create_text(
            l1,
            SensorValueScale.TEXT_HEIGHT_2,
            text=str(profile.extr[0]),
            fill="black",
            font=(Constants.FONT_STYLE.value),
        )
        self.scale_canvas.create_line(
            l1 - 1,
            SensorValueScale.LABEL_LINE_HEIGHT,
            l1 - 1,
            SensorValueScale.LABEL_LINE_HEIGHT
            + SensorValueScale.LABEL_LINE_LENGTH,
            fill="grey",
        )
        self.scale_canvas.create_text(
            l2,
            SensorValueScale.TEXT_HEIGHT_1,
            text=str(profile.extr[1]),
            fill="black",
            font=(Constants.FONT_STYLE.value),
        )
        self.scale_canvas.create_text(
            l3,
            SensorValueScale.TEXT_HEIGHT_2,
            text=str(profile.extr[2]),
            fill="black",
            font=(Constants.FONT_STYLE.value),
        )
        self.scale_canvas.create_line(
            l3 - 1,
            SensorValueScale.LABEL_LINE_HEIGHT,
            l3 - 1,
            SensorValueScale.LABEL_LINE_HEIGHT
            + SensorValueScale.LABEL_LINE_LENGTH,
            fill="grey",
        )
        self.scale_canvas.create_text(
            l4,
            SensorValueScale.TEXT_HEIGHT_1,
            text=str(profile.extr[3]),
            fill="black",
            font=(Constants.FONT_STYLE.value),
        )
        self.scale_canvas.create_text(
            SensorValueScale.WIDTH + SensorValueScale.OFFSET,
            SensorValueScale.TEXT_HEIGHT_2,
            text=str(profile.bound[1]),
            fill="black",
            font=(Constants.FONT_STYLE.value),
        )
        self.scale_canvas.create_line(
            SensorValueScale.WIDTH + SensorValueScale.OFFSET - 1,
            SensorValueScale.LABEL_LINE_HEIGHT,
            SensorValueScale.WIDTH + SensorValueScale.OFFSET - 1,
            SensorValueScale.LABEL_LINE_HEIGHT
            + SensorValueScale.LABEL_LINE_LENGTH,
            fill="grey",
        )

        self.scale_canvas.pack()
        self.scale_frame.pack()

    def update(self, new_value):
        """
        update allows the scale to update
        every time the graph is animated.

        :param new_value:
        :type new_value: Float
        """
        if not new_value:
            new_value = 0
        self.scale_canvas.delete(self.line)
        line = (
            (new_value - self.profile.bound[0]) / self.range_
        ) * SensorValueScale.WIDTH
        self.line = self.scale_canvas.create_line(
            SensorValueScale.OFFSET,
            SensorValueScale.MAIN_LINE_HEIGHT,
            line + SensorValueScale.OFFSET,
            SensorValueScale.MAIN_LINE_HEIGHT,
            width=SensorValueScale.MAIN_LINE_WIDTH,
        )
