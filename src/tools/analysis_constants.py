from enum import Enum


class Analysis_Constants(Enum):

    # Brightness
    BRIGHTNESS_P = 1.2
    BRIGHTNESS_I = 0.5
    BRIGHTNESS_D = 0.001
    BRIGHTNESS_SETPOINT = 270

    # Humidity
    HUMIDITY_P = 1.2
    HUMIDITY_I = 0.5
    HUMIDITY_D = 0.001
    HUMIDITY_SETPOINT = 55

    # Moisture
    MOISTURE_P = 1.2
    MOISTURE_I = 0.5
    MOISTURE_D = 0.001
    MOISTURE_SETPOINT = 50
