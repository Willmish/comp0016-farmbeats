from pubsub import pub
from analyser.analyser import Analyser


class WaterLevelAnalyser(Analyser):
    def __init__(self, *args, **kwargs):
        super().__init__(["sensor_data.water_level_sensor"])

    def analyser_listener(self, args, rest=None):
        MAIN_PUBSUB_TOPIC = "pid_update"  # TODO move to enum/config file
        # 670-2100
        water_level = (
            args.sensor_value
        )  # round(((args.sensor_value * 3300) / 1024), 0)
        sensor_data = args
        if water_level < 50:
            # Send info to gui
            print("low water capacity. ")
        else:
            print("normal water capacity. ")
        # TODO consider changing this structure, as it has no actuator!
        sensor_data.actuator_value = (
            -1
        )  # Set actuator to -1 to avoid null values in DB
        pub.sendMessage(
            f"{MAIN_PUBSUB_TOPIC}.actuator.water_level", args=sensor_data
        )
        print(sensor_data)

    def datastream_update_listener(self, args, rest=None):
        MAIN_PUBSUB_TOPIC = "database_update"
        sensor_data = args
        sensor_data.actuator_value = -1
        pub.sendMessage(
            f"{MAIN_PUBSUB_TOPIC}.actuator.water_level", args=sensor_data
        )
