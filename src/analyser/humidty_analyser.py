from pubsub import pub
from analyser.analyser import Analyser


class HumidityAnalyser(Analyser):
    def __init__(self, *args, **kwargs):
        super().__init__(["sensor_data.humidity_sensor"])

    def analyser_listener(self, args, rest=None):
        sensor_data = args
        humidity = args.sensor_value
        # TODO Do analysing stuff here, currently simple threshold
        if humidity > 80:
            sensor_data.actuator_value = 100
            pub.sendMessage(
                "actuator.fans_status", args=sensor_data
            )  # Fans 50% on
        elif humidity > 70:
            sensor_data.actuator_value = 70
            pub.sendMessage(
                "actuator.fans_status", args=sensor_data
            )  # Fans 20% on
        else:
            sensor_data.actuator_value = 0
            pub.sendMessage("actuator.fans_status", args=sensor_data)
            # FailsafeDefault value (for safety reasons,
            # keep it as 0, as per our security module :)
