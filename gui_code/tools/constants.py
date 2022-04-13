from enum import Enum


class Constants(Enum):
    """
    Constants contain constants that are used across all
    python files in the gui_code folder.

    :param Enum: class for creating enumerated constants.
    :type Enum: Enum
    """

    PADDING = 15
    BACKGROUND = "#E7F5EF"
    GREEN_RGB = "#64975E"
    AMBER_RGB = "#D2A833"
    RED_RGB = "#C34A4D"
    BLUE_RGB = "#B7DEF2"
    TIME_INTERVAL = 1
    RED_LOWER = 0
    AMBER_LOWER = 1
    GREEN = 2
    AMBER_UPPER = 3
    RED_UPPER = 4
    NO_STATUS = 5
    FONT_SIZE = 15
    FONT_STYLE = "Courier"
