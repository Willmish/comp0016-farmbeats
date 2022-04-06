import configparser


def get_list(string):
    if len(string) > 0:
        substring = string[1:-1]
        return [int(x) for x in substring.split(",")]
    else:
        return []

config = configparser.ConfigParser()
config.read("tools/plant_profile_info.ini")
plant_info = config["Plant Information"]
brightness_extr = get_list(plant_info["brightness_extr"])
brightness_bound = get_list(plant_info["brightness_bound"])
brightness_unit = plant_info["brightness_unit"]
humidity_extr = get_list(plant_info["humidity_extr"])
humidity_bound = get_list(plant_info["humidity_bound"])
humidity_unit = plant_info["humidity_unit"]
temperature_extr = get_list(plant_info["temperature_extr"])
temperature_bound = get_list(plant_info["temperature_bound"])
temperature_unit = plant_info["temperature_unit"]
water_level_extr = get_list(plant_info["water_level_extr"])
water_level_bound = get_list(plant_info["water_level_bound"])
water_level_unit = plant_info["water_level_unit"]
