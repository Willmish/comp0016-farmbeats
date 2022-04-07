from profile_view.message_manager import MessageManager
from data_streamer.gui_database_manager import GuiDatabaseManager
from tools.constants import Constants
from tools.config import Config


class ProfileInformation:
    """
    ProfileInformation creates a profile that allows
    GUI to access profile information for each subsystem.
    """

    def __init__(self, profile_name: str, db: GuiDatabaseManager):
        """
        __init__ creates a ProfileInformation instance.

        :param profile_name: Name of subsystem selected.
        :type profile_name: str
        :param db: Instance of GuiDatabaseManager used to
            communicate with the azure database.
        :type db: GuiDatabaseManager
        """
        config = Config()
        self.title = profile_name
        self._db_manager: GuiDatabaseManager() = db
        if profile_name == "Brightness":
            self.sensor_frame_title = "Light Sensor Information"
            self.sensor_value = self._db_manager.get_curr_val_single_subsys(
                "brightness"
            )
            self.unit = config.brightness_unit
            self.sensor_value_description = (
                "Current value: " + str(self.sensor_value) + self.unit
            )

            self.extr = config.brightness_extr
            self.bound = config.brightness_bound

            self.time_list = self._db_manager.get_time_and_val_list(
                "brightness"
            )[1]
            self.val_list = self._db_manager.get_time_and_val_list(
                "brightness"
            )[0]
            self.graph_title = "Brightness over Time"

            self.actuator_frame_title = "LED light Information"
            self.actuator_value = (
                self._db_manager.get_curr_actuation_val_single_subsys(
                    "brightness"
                )
            )

        elif profile_name == "Humidity":
            self.sensor_frame_title = "DH11 Sensor Information"
            self.sensor_value = self._db_manager.get_curr_val_single_subsys(
                "humidity"
            )
            self.unit = config.humidity_unit
            self.sensor_value_description = (
                "Current value: " + str(self.sensor_value) + self.unit
            )

            self.extr = config.humidity_extr
            self.bound = config.humidity_bound

            self.time_list = self._db_manager.get_time_and_val_list(
                "humidity"
            )[1]
            self.val_list = self._db_manager.get_time_and_val_list("humidity")[
                0
            ]
            self.graph_title = "Humidity over Time"

            self.actuator_frame_title = "Fan Information"
            self.actuator_value = (
                self._db_manager.get_curr_actuation_val_single_subsys(
                    "humidity"
                )
            )
        elif profile_name == "Temperature":
            self.sensor_frame_title = "DH11 Sensor Information"
            self.sensor_value = self._db_manager.get_curr_val_single_subsys(
                "temperature"
            )

            self.unit = config.temperature_unit
            self.sensor_value_description = (
                "Current value: " + str(self.sensor_value) + self.unit
            )

            self.extr = config.temperature_extr
            self.bound = config.temperature_bound

            self.time_list = self._db_manager.get_time_and_val_list(
                "temperature"
            )[1]
            self.val_list = self._db_manager.get_time_and_val_list(
                "temperature"
            )[0]
            self.graph_title = "Temperature over Time"

            self.actuator_frame_title = "Heater Information"
            self.actuator_value = (
                self._db_manager.get_curr_actuation_val_single_subsys(
                    "temperature"
                )
            )
        elif profile_name == "Soil Moisture":
            self.sensor_frame_title = "Soil moisture Sensor Information"
            self.sensor_value = self._db_manager.get_curr_val_single_subsys(
                "soil_moisture"
            )
            self.unit = config.water_level_unit
            self.sensor_value_description = (
                "Current value: " + str(self.sensor_value) + self.unit
            )
            self.water_level_value = (
                self._db_manager.get_curr_val_single_subsys("water_level")
            )

            self.extr = config.water_level_extr
            self.bound = config.water_level_bound

            self.time_list = self._db_manager.get_time_and_val_list(
                "soil_moisture"
            )[1]
            self.val_list = self._db_manager.get_time_and_val_list(
                "soil_moisture"
            )[0]
            self.graph_title = "Soil Moisture over Time"

            self.actuator_frame_title = "Sprinkler Information"
            self.actuator_value = (
                self._db_manager.get_curr_actuation_val_single_subsys(
                    "soil_moisture"
                )
            )

        self.actuator_value_description = (
            "Actuator Value set to: \n" + str(self.actuator_value) + self.unit
        )
        self.suggestion = MessageManager(
            profile_name, self.get_status()
        ).message

    def update_from_db(self, profile_name: str):
        """
        update_from_db allows information to be
        up to date with the database.

        :param profile_name: Name of subsystem selected.
        :type profile_name: str
        """

        if profile_name == "Brightness":
            self.sensor_value = self._db_manager.get_curr_val_single_subsys(
                "brightness"
            )
            (
                self.val_list,
                self.time_list,
            ) = self._db_manager.get_time_and_val_list("brightness")
            self.actuator_value = (
                self._db_manager.get_curr_actuation_val_single_subsys(
                    "brightness"
                )
            )
        elif profile_name == "Humidity":
            self.sensor_value = self._db_manager.get_curr_val_single_subsys(
                "humidity"
            )
            (
                self.val_list,
                self.time_list,
            ) = self._db_manager.get_time_and_val_list("humidity")
            self.actuator_value = (
                self._db_manager.get_curr_actuation_val_single_subsys(
                    "humidity"
                )
            )
        elif profile_name == "Temperature":
            self.sensor_value = self._db_manager.get_curr_val_single_subsys(
                "temperature"
            )
            (
                self.val_list,
                self.time_list,
            ) = self._db_manager.get_time_and_val_list("temperature")
            self.actuator_value = (
                self._db_manager.get_curr_actuation_val_single_subsys(
                    "temperature"
                )
            )
        elif profile_name == "Soil Moisture":
            self.sensor_value = self._db_manager.get_curr_val_single_subsys(
                "soil_moisture"
            )
            self.water_level_value = (
                self._db_manager.get_curr_val_single_subsys("water_level")
            )
            (
                self.val_list,
                self.time_list,
            ) = self._db_manager.get_time_and_val_list("soil_moisture")
            self.actuator_value = (
                self._db_manager.get_curr_actuation_val_single_subsys(
                    "soil_moisture"
                )
            )
        self.sensor_value_description = (
            "Current value: " + str(self.sensor_value) + self.unit
        )
        self.actuator_value_description = (
            "Actuator Value set to: \n" + str(self.actuator_value) + self.unit
        )
        self.suggestion = MessageManager(
            profile_name, self.get_status()
        ).message

    def get_status(self) -> int:
        """
        get_status returns the state for the message
        manager to output the correct message.

        :return: Integer representing whether status
            is green, red or amber.
        :rtype: int
        """
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
