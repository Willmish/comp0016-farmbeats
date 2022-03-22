from profile_view.message_manager import MessageManager
from data_streamer.gui_database_manager import GuiDatabaseManager
from tools.constants import Constants


class ProfileInformation:
    def __init__(self, profile_name, db: GuiDatabaseManager):
        self.title = profile_name
        self._db_manager: GuiDatabaseManager() = db
        if profile_name == "Brightness":
            self.sensor_frame_title = "Light Sensor Information"
            self.sensor_value = self._db_manager.get_curr_val_single_subsys("brightness")
            self.unit = "cd"
            self.sensor_value_description = (
                "Current value: " + str(self.sensor_value) + self.unit
            )

            # [extreme_lower, lower, upper, extreme_upper]
            self.extr = [100, 200, 250, 400]
            self.bound = [0, 500]

            self.time_list = self._db_manager.get_time_and_val_list("brightness")[1]
            self.val_list = self._db_manager.get_time_and_val_list("brightness")[0]
            self.graph_title = "Brightness over Time"

            self.actuator_frame_title = "LED light Information"
            self.actuator_value = self._db_manager.get_curr_actuation_val_single_subsys(
                "brightness"
            )
            self.actuator_value_description = (
                "Brightness set to: \n"
                + str(self.actuator_value)
                + self.unit
            )

        elif profile_name == "Humidity":
            self.sensor_frame_title = "DH11 Sensor Information"
            self.sensor_value = self._db_manager.get_curr_val_single_subsys("humidity")
            self.unit = "%"
            self.sensor_value_description = (
                "Current value: " + str(self.sensor_value) + self.unit
            )

            # [extreme_lower, lower, upper, extreme_upper]
            self.extr = [50, 60, 70, 80]
            self.bound = [0, 100]

            self.time_list = self._db_manager.get_time_and_val_list("humidity")[1]
            self.val_list = self._db_manager.get_time_and_val_list("humidity")[0]
            self.graph_title = "Humidity over Time"

            self.actuator_frame_title = "Fan Information"
            self.actuator_value = self._db_manager.get_curr_actuation_val_single_subsys(
                "humidity"
            )
            self.actuator_value_description = (
                "Input speed set to: \n"
                + str(self.actuator_value)
                + self.unit
                + "\n Output speed set to: "
                + str(self.actuator_value)
                + self.unit
            )

        elif profile_name == "Temperature":
            self.sensor_frame_title = "DH11 Sensor Information"
            self.sensor_value = self._db_manager.get_curr_val_single_subsys(
                "temperature"
            )

            self.unit = "°c"
            self.sensor_value_description = (
                "Current value: " + str(self.sensor_value) + self.unit
            )

            # [extreme_lower, lower, upper, extreme_upper]
            self.extr = [10, 16, 25, 30]
            self.bound = [0, 40]

            self.time_list = self._db_manager.get_time_and_val_list("temperature")[1]
            self.val_list = self._db_manager.get_time_and_val_list("temperature")[0]
            self.graph_title = "Temperature over Time"

            self.actuator_frame_title = "Heater Information"
            self.actuator_value = self._db_manager.get_curr_actuation_val_single_subsys(
                "temperature"
            )
            self.actuator_value_description = (
                "Heater set to: \n" + str(self.actuator_value) + self.unit
            )
        elif profile_name == "Water Level":
            self.sensor_frame_title = "Soil moisture Sensor Information"
            self.sensor_value = self._db_manager.get_curr_val_single_subsys(
                "soil moisture"
            )
            self.unit = "%"
            self.sensor_value_description = (
                "Current value: " + str(self.sensor_value) + self.unit
            )
            self.water_level_value = self._db_manager.get_curr_val_single_subsys(
                "water level"
            )

            # [extreme_lower, lower, upper, extreme_upper]
            self.extr = [10, 18, 44, 50]
            self.bound = [0, 100]

            self.time_list = self._db_manager.get_time_and_val_list("water level")[1]
            self.val_list = self._db_manager.get_time_and_val_list("water level")[0]
            self.graph_title = "Soil Moisture over Time"

            self.actuator_frame_title = "Sprinkler Information"
            self.actuator_value = self._db_manager.get_curr_actuation_val_single_subsys(
                "water level"
            )
            self.actuator_value_description = (
                "Amount of water added: \n"
                + str(self.actuator_value)
                + self.unit
            )
        self.suggestion = MessageManager(
            profile_name, self.get_status()
        ).message

    def update_from_db(self, profile_name):
        if profile_name == "Brightness":
            self.sensor_value = self._db_manager.get_curr_val_single_subsys("brightness")
            self.val_list, self.time_list = self._db_manager.get_time_and_val_list("brightness")
            self.actuator_value = self._db_manager.get_curr_actuation_val_single_subsys(
                "brightness"
            )
        elif profile_name == "Humidity":
            self.sensor_value = self._db_manager.get_curr_val_single_subsys("humidity")
            self.val_list, self.time_list = self._db_manager.get_time_and_val_list("humidity")
            self.actuator_value = self._db_manager.get_curr_actuation_val_single_subsys(
                "humidity"
            )
        elif profile_name == "Temperature":
            self.sensor_value = self._db_manager.get_curr_val_single_subsys(
                "temperature"
            )
            self.val_list, self.time_list = self._db_manager.get_time_and_val_list("temperature")
            self.actuator_value = self._db_manager.get_curr_actuation_val_single_subsys(
                "temperature"
            )
        elif profile_name == "Water Level":
            self.sensor_value = self._db_manager.get_curr_val_single_subsys(
                "soil moisture"
            )
            self.water_level_value = self._db_manager.get_curr_actuation_val_single_subsys(
                "water_level"
            )
            self.val_list, self.time_list = self._db_manager.get_time_and_val_list("water_level")
            self.actuator_value = self._db_manager.get_curr_actuation_val_single_subsys(
                "water_level"
            )
        self.sensor_value_description = (
            "Current value: " + str(self.sensor_value) + self.unit
        )
        self.actuator_value_description = (
            "Actuator Value set to: \n"
            + str(self.actuator_value)
            + self.unit
        )

    def get_status(self):
        if self.sensor_value:
            if self.sensor_value < self.extr[0]:
                return Constants.RED_LOWER.value
            elif self.sensor_value < self.extr[1]:
                return Constants.AMBER_LOWER.value
            elif self.sensor_value < self.extr[2]:
                return Constants.GREEN.value
            elif self.sensor_value < self.extr[3]:
                return Constants.AMBER_UPPER.value
            else:
                return Constants.RED_UPPER.value
        else:
            return Constants.NO_STATUS.value
