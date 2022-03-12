from pubsub import pub
from analyser.analyser import Analyser


class BrightnessAnalyser(Analyser):
    def __init__(self, *args, **kwargs):
        super().__init__(["sensor_data.light_sensor"])

    def analyser_listener(self, args, rest=None):
        print(args.sensor_value)
        sensor_data = args
        brightness = args.sensor_value
        # TODO Do analysing stuff here, currently simple threshold
        print(brightness)
        if brightness > 270:
            sensor_data.actuator_value = 0.5
            pub.sendMessage(
                "actuator.light_status", args=sensor_data
            )  # Lights 50% on
        elif brightness > 270:
            sensor_data.actuator_value = 0.2
            pub.sendMessage(
                "actuator.light_status", args=sensor_data
            )  # Lights 20% on
        else:
            sensor_data.actuator_value = 0
            pub.sendMessage("actuator.light_status", args=sensor_data)
