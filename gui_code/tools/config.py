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
        self.brightness_unit = None
        self.humidity_extr = None
        self.humidity_bound = None
        self.humidity_unit = None
        self.temperature_extr = None
        self.temperature_bound = None
        self.temperature_unit = None
        self.water_level_extr = None
        self.water_level_bound = None
        self.water_level_unit = None

        if ConfigFileParser(filename).valid:
            self.set_values(filename)
        else:
            with open("tools/default_plant_profile_info.ini", "r") as input:
                with open("tools/plant_profile_info.ini", "w+") as f:
                    f.write(input.read())
                    self.set_values(filename)
            print ("RESET")

    def set_values(self, filename):
        self.config = configparser.ConfigParser()
        self.config.read(filename)
        self.plant_info = self.config["Plant Information"]
        self.name = self.plant_info["name"]
        self.brightness_extr = self.get_list(self.plant_info["brightness_extr"])
        self.brightness_bound = self.get_list(self.plant_info["brightness_bound"])
        self.brightness_unit = self.plant_info["brightness_unit"]
        self.humidity_extr = self.get_list(self.plant_info["humidity_extr"])
        self.humidity_bound = self.get_list(self.plant_info["humidity_bound"])
        self.humidity_unit = self.plant_info["humidity_unit"]
        self.temperature_extr = self.get_list(self.plant_info["temperature_extr"])
        self.temperature_bound = self.get_list(self.plant_info["temperature_bound"])
        self.temperature_unit = self.plant_info["temperature_unit"]
        self.water_level_extr = self.get_list(self.plant_info["water_level_extr"])
        self.water_level_bound = self.get_list(self.plant_info["water_level_bound"])
        self.water_level_unit = self.plant_info["water_level_unit"]


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

    def check_val(self, type, value):
        if len(value.strip(" ")) >0:
            if type == "str":
                return True
            else:
                if value[0] == '[' and value[-1] == ']':
                    if type == "list4":
                         if len( value[1:-1].split(",")) == 4 and self.get_list(value):
                            return True
                    elif type =="list2":
                         if len( value[1:-1].split(",")) == 2 and self.get_list(value):
                            return True
            return False
        else:
            return False
    def parse(self, dict):
        dict_structure = {
            "name": "str",
            "brightness_extr": "list4",
            "brightness_bound": "list2",
            "brightness_unit": "str",
            "humidity_extr": "list4",
            "humidity_bound": "list2",
            "humidity_unit": "str",
            "temperature_extr": "list4",
            "temperature_bound": "list2",
            "temperature_unit": "str",
            "water_level_extr": "list4",
            "water_level_bound":  "list2",
            "water_level_unit": "str",
            }
        valid = True

        if list(dict.keys()) == list(dict_structure.keys()):
            for i in range(len(dict.values())):
                if not self.check_val(list(dict_structure.values())[i], list(dict.values())[i]):
                    valid = False
        else:
            valid = False
        return valid
Config()