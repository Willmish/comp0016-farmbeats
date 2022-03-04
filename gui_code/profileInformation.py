from gui_database_manager import GuiDatabaseManager

INPUT = 800
LOWER = 700
UPPER = 850
EXLOWER = 600
EXUPPER = 950
ACTUATION = 900
MESSAGE = "The sensor readings seem good!"
LOWER_BOUND = 0
UPPER_BOUND = 1000
TIMELIST = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45]
VALUELIST = [904, 920, 911, 890, 883, 880, 881, 860, 872, 888]


class ProfileInformation:
    def __init__(self, profile_name):
        with GuiDatabaseManager() as db:
            self.title = profile_name
            if profile_name == "Brightness":
                self.sensor_frame_title = "Light Sensor Information"
                self.sensor_value = db.get_curr_val_single_subsys("brightness")
                self.unit = "cd"
                self.sensor_value_description = (
                    "Current value: " + str(self.sensor_value) + self.unit
                )

                # [extreme_lower, lower, upper, extreme_upper]
                self.extr = [EXLOWER, LOWER, UPPER, EXUPPER]
                self.bound = [LOWER_BOUND, UPPER_BOUND]

                self.time_list = db.get_time_and_val_list("brightness")[1]
                self.val_list = db.get_time_and_val_list("brightness")[0]
                self.graph_title = "Brightness over Time"

                self.actuator_frame_title = "LED light Information"
                self.actuator_value = ACTUATION
                self.actuator_value_description = (
                    "Brightness set to: \n"
                    + str(self.actuator_value)
                    + self.unit
                )

                self.suggestion = MESSAGE

            elif profile_name == "Humidity":
                self.sensor_frame_title = "DH11 Sensor Information"
                self.sensor_value = db.get_curr_val_single_subsys("humidity")
                self.unit = "%"
                self.sensor_value_description = (
                    "Current value: "
                    + str(self.sensor_value)
                    + self.unit
                )

                # [extreme_lower, lower, upper, extreme_upper]
                self.extr = [EXLOWER, LOWER, UPPER, EXUPPER]
                self.bound = [LOWER_BOUND, UPPER_BOUND]

                self.time_list = db.get_time_and_val_list("humidity")[1]
                self.val_list = db.get_time_and_val_list("humidity")[0]
                self.graph_title = "Humidity over Time"

                self.actuator_frame_title = "Fan Information"
                self.actuator_value = ACTUATION
                self.actuator_value_description = (
                    "Input speed set to: \n"
                    + str(self.actuator_value)
                    + self.unit
                    + "\n Output speed set to: "
                    + str(self.actuator_value)
                    + self.unit
                )

                self.suggestion = MESSAGE

            elif profile_name == "Temperature":
                self.sensor_frame_title = "DH11 Sensor Information"
                self.sensor_value = \
                    db.get_curr_val_single_subsys("temperature")

                self.unit = "°c"
                self.sensor_value_description = (
                    "Current value: "
                    + str(self.sensor_value)
                    + self.unit
                )

                # [extreme_lower, lower, upper, extreme_upper]
                self.extr = [EXLOWER, LOWER, UPPER, EXUPPER]
                self.bound = [LOWER_BOUND, UPPER_BOUND]

                self.time_list = db.get_time_and_val_list("temperature")[1]
                self.val_list = db.get_time_and_val_list("temperature")[0]
                self.graph_title = "Temperature over Time"

                self.actuator_frame_title = "Heater Information"
                self.actuator_value = ACTUATION
                self.actuator_value_description = (
                    "Heater set to: \n"
                    + str(self.actuator_value)
                    + self.unit
                )

                self.suggestion = MESSAGE
            elif profile_name == "Water":
                self.sensor_frame_title = \
                    "Soil moisture Sensor Information"
                self.sensor_value = \
                    db.get_curr_val_single_subsys("water level")
                self.unit = "%"
                self.sensor_value_description = (
                    "Current value: "
                    + str(self.sensor_value)
                    + self.unit
                )

                # [extreme_lower, lower, upper, extreme_upper]
                self.extr = [EXLOWER, LOWER, UPPER, EXUPPER]
                self.bound = [LOWER_BOUND, UPPER_BOUND]

                self.time_list = db.get_time_and_val_list("water level")[1]
                self.val_list = db.get_time_and_val_list("water level")[0]
                self.graph_title = "Soil Moisture over Time"

                self.actuator_frame_title = "Sprinkler Information"
                self.actuator_value = ACTUATION
                self.actuator_value_description = (
                    "Amount of water added: \n"
                    + str(self.actuator_value)
                    + self.unit
                )

                self.suggestion = MESSAGE
