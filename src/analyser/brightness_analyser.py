from pubsub import pub
from analyser.analyser import Analyser
import tools.config as config


class BrightnessAnalyser(Analyser):
    def __init__(self, *args, **kwargs):
        super().__init__(["sensor_data.light_sensor"])

    def analyser_listener(self, args, rest=None):
        MAIN_PUBSUB_TOPIC = "pid_update"  # TODO move to enum/config file
        print(args.sensor_value)
        sensor_data = args
        brightness = args.sensor_value
        # TODO Do analysing stuff here, currently simple threshold
        print(brightness)
        if brightness > 270:
            sensor_data.actuator_value = 0.5
            pub.sendMessage(
                f"{MAIN_PUBSUB_TOPIC}.{config.actuator}.{config.light_status}",
                args=sensor_data,
            )  # Lights 50% on
        elif brightness > 270:
            sensor_data.actuator_value = 0.2
            pub.sendMessage(
                f"{MAIN_PUBSUB_TOPIC}.{config.actuator}.{config.light_status}",
                args=sensor_data,
            )  # Lights 20% on
        else:
            sensor_data.actuator_value = 0
            pub.sendMessage(
                f"{MAIN_PUBSUB_TOPIC}.{config.actuator}.{config.light_status}",
                args=sensor_data,
            )

    def analyser_datastream_update_listener(self, args, rest=None):
        pass
