import configparser

config = configparser.ConfigParser()
config.read("config.ini")
sensor = config["SENSOR"]
status = config["STATUS"]
actuator = config["ACTUATOR"]
