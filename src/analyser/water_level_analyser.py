from pubsub import pub
from analyser.analyser import Analyser
from tools.logging import logDebug


class WaterLevelAnalyser(Analyser):
    def __init__(self, *args, **kwargs):
        super().__init__(["sensor_data.water_level_sensor"])

    def analyser_listener(self, args, rest=None):
        MAIN_PUBSUB_TOPIC = "pid_update"
        # Water level sensor range: 670-2100
        sensor_data = args
        sensor_data.actuator_value = (
            -1
        )  # Set actuator to -1 to avoid null values in DB
        logDebug(f"{sensor_data}")
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
