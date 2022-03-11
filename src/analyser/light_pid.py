from pubsub import pub
from analyser.analyser import Analyser
from pid.pid import PID
import time


class LightPidAnalyser(Analyser):
    def __init__(self, *args, **kwargs):
        super().__init__(["sensor_data.light_sensor"])

    def analyser_listener(self, args, rest=None):
        print(args.sensor_value)
        brightness = args.sensor_value
        # TODO Do analysing stuff here, currently simple threshold
        print(brightness)
        p = 1.2
        i = 0.5
        d = 0.001
        clock = 5
        pid = PID(p, i, d)
        pid.SetPoint = 270
        while True:
            feedback = brightness
            pid.update(feedback)
            output = (100 - pid.output)/100  # fill in maximam sensor number
            pub.sendMessage("actuator.light_status", args=output)  # pump on
            time.sleep(clock)