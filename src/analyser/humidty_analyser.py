from pubsub import pub
from analyser.analyser import Analyser


class HumidityAnalyser(Analyser):
    def __init__(self, *args, **kwargs):
        super().__init__(["humidity_sensor"])

    def analyser_listener(self, args, rest=None):
        humidity = args
        # TODO Do analysing stuff here, currently simple threshold
        if humidity > 0.7:
            pub.sendMessage("fans_status", 0.5)  # Fans 50% on
        elif humidity > 0.5:
            pub.sendMessage("fans_status", 0.2)  # Fans 20% on
        else:
            pub.sendMessage("fans_status", 0.0)
            # FailsafeDefault value (for safety reasons,
            # keep it as 0, as per our security module :)
