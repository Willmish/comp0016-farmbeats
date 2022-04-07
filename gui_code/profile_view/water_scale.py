from tkinter import Frame
import tkinter
from tools.constants import Constants


class WaterScale:
    """
    WaterScale creates and displays the water scale on water frame.
    """

    CANVAS_HEIGHT = 200
    CANVAS_WIDTH = 80
    CONTAINER_HEIGHT = 200
    CONTAINER_WIDTH = 50
    Y_OFFSET = 20
    X_OFFSET = 10
    TEXT_Y_OFFSET = 5
    TEXT_X_OFFSET = 10
    LINE_WIDTH = 3

    def __init__(self, water_level_frame, water_level_value):
        """
        __init__ creates a WaterScale instance.

        :param water_level_frame: Frame to contain scale canvas.
        :type water_level_frame: Frame
        :param water_level_value: Current water level percentage value.
        :type water_level_value: float
        """

        self.scale_frame = Frame(water_level_frame)

        self.scale_canvas = tkinter.Canvas(
            self.scale_frame,
            height=WaterScale.CANVAS_HEIGHT + WaterScale.Y_OFFSET,
            width=WaterScale.CANVAS_WIDTH + (2 * WaterScale.X_OFFSET),
        )

        self.length = self.calculate_water_level_length(water_level_value)

        self.scale_canvas.create_rectangle(
            WaterScale.X_OFFSET,
            WaterScale.Y_OFFSET,
            WaterScale.CONTAINER_WIDTH + WaterScale.X_OFFSET,
            WaterScale.CONTAINER_HEIGHT + WaterScale.Y_OFFSET,
            width=0,
        )

        self.draw_scale()

        self.scale_canvas.create_text(
            WaterScale.CONTAINER_WIDTH
            + (2 * WaterScale.X_OFFSET)
            + WaterScale.TEXT_X_OFFSET,
            WaterScale.Y_OFFSET,
            text="100%",
            fill="black",
            font=(Constants.FONT_STYLE.value),
        )
        self.scale_canvas.create_text(
            WaterScale.CONTAINER_WIDTH
            + (2 * WaterScale.X_OFFSET)
            + WaterScale.TEXT_X_OFFSET,
            WaterScale.CONTAINER_HEIGHT // 2
            + WaterScale.Y_OFFSET
            - WaterScale.TEXT_Y_OFFSET,
            text="50%",
            fill="black",
            font=(Constants.FONT_STYLE.value),
        )
        self.scale_canvas.create_text(
            WaterScale.CONTAINER_WIDTH
            + (2 * WaterScale.X_OFFSET)
            + WaterScale.TEXT_X_OFFSET,
            WaterScale.CONTAINER_HEIGHT
            + WaterScale.Y_OFFSET
            - WaterScale.TEXT_Y_OFFSET,
            text="0%",
            fill="black",
            font=(Constants.FONT_STYLE.value),
        )

        self.scale_canvas.pack()
        self.scale_frame.grid(
            row=1,
            column=0,
            sticky="news",
            padx=Constants.PADDING.value,
        )

    def draw_scale(self):
        self.water_level_rect = self.scale_canvas.create_rectangle(
            WaterScale.X_OFFSET,
            WaterScale.CONTAINER_HEIGHT + WaterScale.Y_OFFSET,
            WaterScale.CONTAINER_WIDTH + WaterScale.X_OFFSET,
            WaterScale.CONTAINER_HEIGHT - self.length + WaterScale.Y_OFFSET,
            fill=Constants.BLUE_RGB.value,
            width=0,
        )
        self.left_line = self.scale_canvas.create_line(
            WaterScale.X_OFFSET,
            WaterScale.CONTAINER_HEIGHT + WaterScale.Y_OFFSET,
            WaterScale.X_OFFSET,
            WaterScale.Y_OFFSET,
            fill="black",
            width=3,
        )
        self.right_line = self.scale_canvas.create_line(
            WaterScale.CONTAINER_WIDTH + WaterScale.X_OFFSET - 1,
            WaterScale.CONTAINER_HEIGHT + WaterScale.Y_OFFSET,
            WaterScale.CONTAINER_WIDTH + WaterScale.X_OFFSET - 1,
            WaterScale.Y_OFFSET,
            fill="black",
            width=WaterScale.LINE_WIDTH,
        )
        self.bottom_line = self.scale_canvas.create_line(
            WaterScale.CONTAINER_WIDTH + WaterScale.X_OFFSET,
            WaterScale.CONTAINER_HEIGHT + WaterScale.Y_OFFSET,
            WaterScale.X_OFFSET,
            WaterScale.CONTAINER_HEIGHT + WaterScale.Y_OFFSET,
            fill="black",
            width=WaterScale.LINE_WIDTH,
        )

    def calculate_water_level_length(self, water_level_value: float) -> float:
        """
        calculate_water_level_length returns length of line scaled
        from water_level_value.

        :param water_level_value: Percentage of water level.
        :type water_level_value: float
        :return: Scaled value.
        :rtype: fload
        """
        return (water_level_value / 100) * WaterScale.CONTAINER_HEIGHT

    def update(self, new_value):
        """
        update allows the scale to update
        every time the graph is animated.

        :param new_value: New current value to be
            displayed on scale.
        :type new_value: float
        """
        if not new_value:
            new_value = 0
        self.scale_canvas.delete(self.water_level_rect)
        self.scale_canvas.delete(self.left_line)
        self.scale_canvas.delete(self.right_line)
        self.scale_canvas.delete(self.bottom_line)
        self.length = self.calculate_water_level_length(new_value)
        self.draw_scale()
