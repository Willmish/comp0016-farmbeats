from pubsub import pub
from analyser.analyser import Analyser


class BrightnessAnalyser(Analyser):
    def __init__(self, *args, **kwargs):
        super().__init__(["sensor_data.light_sensor"])

    def analyser_listener(self, args, rest=None):
        data = args
        print(args.sensor_value)
        brightness = args.sensor_value[0]
        # TODO Do analysing stuff here, currently simple threshold
        print(brightness)
        if brightness > 270:
            pub.sendMessage("actuator.light_status", args=0.5)  # Lights 50% on
        elif brightness > 270:
            pub.sendMessage("actuator.light_status", args=0.2)  # Lights 20% on
        else:
            pub.sendMessage("actuator.light_status", args=0.0)
            # FailsafeDefault value (for safety reasons,
            # keep it as 0, as per our security module :)
