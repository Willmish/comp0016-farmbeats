from pubsub import pub
from analyser.analyser import Analyser
import tools.config

class HumidityAnalyser(Analyser):
    def __init__(self, *args, **kwargs):
        super().__init__([tools.config.sensor['humidity_sensor']])

    def analyser_listener(self, args, rest=None):
        sensor_data = args
        humidity = args.sensor_value
        # TODO Do analysing stuff here, currently simple threshold
        if humidity > 80:
            sensor_data.actuator_value = 100
            pub.sendMessage(
                tools.config.status['humidity_status'], args=sensor_data
            )  # Fans 50% on
        elif humidity > 70:
            sensor_data.actuator_value = 70
            pub.sendMessage(
                tools.config.status['humidity_status'], args=sensor_data
            )  # Fans 20% on
        else:
            sensor_data.actuator_value = 0
            pub.sendMessage(tools.config.status['humidity_status'], args=sensor_data)
