from pubsub import pub
from analyser.analyser import Analyser


class WaterLevelAnalyser(Analyser):
    def __init__(self, *args, **kwargs):
        super().__init__(["sensor_data.water_level_sensor"])

    def analyser_listener(self, args, rest=None):
        voltage = round(((soilmoisture * 3300) / 1024), 0)
        if voltage < 50:
            # Send info to gui
            print("low water capacity. ")
        else:
            print("normal water capacity. ")

    def analyser_listener(self, args, rest=None):
        MAIN_PUBSUB_TOPIC = "pid_update"  # TODO move to enum/config file
        water_level =round(((args.sensor_value * 3300) / 1024), 0)
        sensor_data = args
        if water_level < 50:
            # Send info to gui
            print("low water capacity. ")
        else:
            print("normal water capacity. ")
        # TODO consider changing this structure, as it has no actuator!
        pub.sendMessage(f"{MAIN_PUBSUB_TOPIC}.actuator.water_level", args=sensor_data)

    def datastream_update_listener(self, args, rest=None):
        MAIN_PUBSUB_TOPIC = "database_update"
        sensor_data = args
        pub.sendMessage(f"{MAIN_PUBSUB_TOPIC}.actuator.water_level", args=sensor_data)