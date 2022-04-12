import configparser
from logging import exception
from typing import List

from tools.config_file_parser import ConfigFileParser


class Config:
    """
    Config class accesses information from plant_profile_info.ini
    file and stores them as attributes.
    """

    def __init__(self):
        """
        __init__ creates an instance of Config.
        """
        filename= "tools/plant_profile_info.ini"
        self.config = None
        self.plant_info = None
        self.name = None
        self.brightness_extr = None
        self.brightness_bound = None
        self.brightness_sensor_unit = None
        self.brightness_actuator_unit = None
        self.humidity_extr = None
        self.humidity_bound = None
        self.humidity_sensor_unit = None
        self.humidity_actuator_unit = None
        self.temperature_extr = None
        self.temperature_bound = None
        self.temperature_sensor_unit = None
        self.temperature_actuator_unit = None
        self.water_level_extr = None
        self.water_level_bound = None
        self.water_level_sensor_unit = None
        self.water_level_actuator_unit = None

        if ConfigFileParser(filename).valid:
            self.set_values(filename)
        else:
            with open("tools/default_plant_profile_info.ini", "r") as input:
                with open("tools/plant_profile_info.ini", "w+") as f:
                    f.write(input.read())
                    self.set_values(filename)

    def set_values(self, filename):
        self.config = configparser.ConfigParser()
        self.config.read(filename)
        self.plant_info = self.config["Plant Information"]
        self.name = self.plant_info["name"]
        self.brightness_extr = self.get_list(self.plant_info["brightness_extr"])
        self.brightness_bound = self.get_list(self.plant_info["brightness_bound"])
        self.brightness_sensor_unit = self.plant_info["brightness_sensor_unit"]
        self.brightness_actuator_unit = self.plant_info["brightness_actuator_unit"]
        self.humidity_extr = self.get_list(self.plant_info["humidity_extr"])
        self.humidity_bound = self.get_list(self.plant_info["humidity_bound"])
        self.humidity_sensor_unit = self.plant_info["humidity_sensor_unit"]
        self.humidity_actuator_unit = self.plant_info["humidity_actuator_unit"]
        self.temperature_extr = self.get_list(self.plant_info["temperature_extr"])
        self.temperature_bound = self.get_list(self.plant_info["temperature_bound"])
        self.temperature_sensor_unit = self.plant_info["temperature_sensor_unit"]
        self.temperature_actuator_unit = self.plant_info["temperature_actuator_unit"]
        self.water_level_extr = self.get_list(self.plant_info["water_level_extr"])
        self.water_level_bound = self.get_list(self.plant_info["water_level_bound"])
        self.water_level_sensor_unit = self.plant_info["water_level_sensor_unit"]
        self.water_level_actuator_unit = self.plant_info["water_level_actuator_unit"]


    def get_list(self, string: str) -> List[int]:
        """
        get_list takes a list of type string and
        returns it as type list of integers.

        :param string: List of type string.
        :type string: str
        :return: List of integers converted from string.
        :rtype: list(int)
        """
        if len(string) > 0:
            substring = string[1:-1]
            try:
                return [int(x) for x in substring.split(",")]
            except:
                return None
        else:
            return []
