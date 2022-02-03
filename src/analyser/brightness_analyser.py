from pubsub import pub
from analyser.analyser import Analyser


class BrightnessAnalyser(Analyser):
    def __init__(self, *args, **kwargs):
        super().__init__(["light_sensor"])

    def analyser_listener(self, args, rest=None):
        brightness = args
        # TODO Do analysing stuff here, currently simple threshold
        if brightness > 80:
            pub.sendMessage("light_status", args=0.5)  # Lights 50% on
        elif brightness > 60:
            pub.sendMessage("light_status", args=0.2)  # Lights 20% on
        else:
            pub.sendMessage("light_status", args=0.0)
            # FailsafeDefault value (for safety reasons,
            # keep it as 0, as per our security module :)