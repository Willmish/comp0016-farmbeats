import configparser
from typing import List

class Config:
    """
    Config class accesses information from plant_profile_info.ini
    file and stores them as attributes.
    """


    def __init__(self):
        """
        __init__ creates an instance of Config.
        """
        config = configparser.ConfigParser()
        config.read("tools/plant_profile_info.ini")
        plant_info = config["Plant Information"]
        self.name = plant_info["name"]
        self.brightness_extr = self.get_list(plant_info["brightness_extr"])
        self.brightness_bound = self.get_list(plant_info["brightness_bound"])
        self.brightness_unit = plant_info["brightness_unit"]
        self.humidity_extr = self.get_list(plant_info["humidity_extr"])
        self.humidity_bound = self.get_list(plant_info["humidity_bound"])
        self.humidity_unit = plant_info["humidity_unit"]
        self.temperature_extr = self.get_list(plant_info["temperature_extr"])
        self.temperature_bound = self.get_list(plant_info["temperature_bound"])
        self.temperature_unit = plant_info["temperature_unit"]
        self.water_level_extr = self.get_list(plant_info["water_level_extr"])
        self.water_level_bound = self.get_list(plant_info["water_level_bound"])
        self.water_level_unit = plant_info["water_level_unit"]


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
            return [int(x) for x in substring.split(",")]
        else:
            return []
