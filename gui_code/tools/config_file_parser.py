import configparser
from typing import List


class ConfigFileParser:
    """
    Config class accesses information from plant_profile_info.ini
    file and stores them as attributes.
    """

    def __init__(self, filename):
        """
        __init__ creates an instance of Config.
        """
        config = configparser.ConfigParser()
        config.read(filename)
        self.valid = list(config.sections()) == ["Plant Information"]
        if self.valid:
            plant_info = config["Plant Information"]
            if not self.parse(plant_info):
                self.valid = False

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
            "brightness_sensor_unit": "str",
            "brightness_actuator_unit": "str",
            "humidity_extr": "list4",
            "humidity_bound": "list2",
            "humidity_sensor_unit": "str",
            "humidity_actuator_unit": "str",
            "temperature_extr": "list4",
            "temperature_bound": "list2",
            "temperature_sensor_unit": "str",
            "temperature_actuator_unit": "str",
            "water_level_extr": "list4",
            "water_level_bound":  "list2",
            "water_level_sensor_unit": "str",
            "water_level_actuator_unit": "str",
            }
        valid = True

        if list(dict.keys()) == list(dict_structure.keys()):
            for i in range(len(dict.values())):
                if not self.check_val(list(dict_structure.values())[i], list(dict.values())[i]):
                    valid = False
        else:
            valid = False
        return valid
