from pubsub import pub
from analyser.analyser import Analyser

class WaterAnalyser(Analyser):
    def __init__(self, *args, **kwargs):
        super().__init__(["sensor_data.water_level_sensor"])

    def analyser_listener(self, args, rest=None):
        print(args.sensor_value)
        waterlevel = args.sensor_value
        # TODO Do analysing stuff here, currently simple threshold
        print(waterlevel)
        voltage = round(((waterlevel * 3300) / 1024), 0)
        if voltage < 50:
            pub.sendMessage("actuator.pump_status", args=1)  # Lights 50% on
        else:
            pub.sendMessage("actuator.pump_status", args=0.0)
            # FailsafeDefault value (for safety reasons,
            # keep it as 0, as per our security module :)