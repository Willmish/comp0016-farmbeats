from pubsub import pub
from analyser.analyser import Analyser


class MoistureAnalyser(Analyser):
    def __init__(self, *args, **kwargs):
        super().__init__(["sensor_data.soil_moisture_sensor"])

    def analyser_listener(self, args, rest=None):
        print(args.sensor_value)
        soilmoisture = args.sensor_value
        # TODO Do analysing stuff here, currently simple threshold
        print(soilmoisture)
        voltage = round(((soilmoisture * 3300) / 1024), 0)
        if voltage < 50:
            pub.sendMessage("actuator.pump_status", args=1)
        else:
            pub.sendMessage("actuator.pump_status", args=0.0)
