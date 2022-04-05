import configparser

config = configparser.ConfigParser()
config.read("config.ini")

main_topics = config["MAIN TOPICS"]
sensor_data = main_topics["sensor_data"]
actuator = main_topics["actuator"]
actuator_value = main_topics["actuator_value"]
pid_update = main_topics["pid_update"]
database_update = main_topics["database_update"]

sensor_types = config["SENSOR TYPES"]
light_sensor = sensor_types["light_sensor"]
humidity_sensor = sensor_types["humidity_sensor"]
soil_moisture_sensor = sensor_types["soil_moisture_sensor"]
water_level_sensor = sensor_types["water_level_sensor"]
ambient_temperature_sensor = sensor_types["ambient_temperature_sensor"]

actuator_status = config["ACTUATOR STATUS"]
light_status = actuator_status["light_status"]
fans_status = actuator_status["fans_status"]
water_level = actuator_status["water_level"]
water_pump_status = actuator_status["water_pump_status"]

