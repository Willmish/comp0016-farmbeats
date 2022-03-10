from pubsub import pub
from analyser.analyser import Analyser

class WaterCapacityAnalyser(Analyser):
    def __init__(self, *args, **kwargs):
        super().__init__(["sensor_data.water_level_sensor"])

    def analyser_listener(self, args, rest=None):
        print(args.sensor_value)
        soilmoisture = args.sensor_value
        # TODO Do analysing stuff here, currently simple threshold
        print(soilmoisture)
        voltage = round(((soilmoisture * 3300) / 1024), 0)
        if voltage < 50:
            # Send info to gui
            print("low water capacity. ")
        else:
            print("normal water capacity. ")