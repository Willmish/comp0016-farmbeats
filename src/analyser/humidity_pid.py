from pubsub import pub
from analyser.analyser import Analyser
from pid.pid import PID
import time


class HumidityPidAnalyser(Analyser):
    def __init__(self, *args, **kwargs):
        super().__init__(["sensor_data.humidity_sensor"])

    def analyser_listener(self, args, rest=None):
        print(args.sensor_value)
        humidity = args.sensor_value
        # TODO Do analysing stuff here, currently simple threshold
        print(humidity)
        p = 1.2
        i = 0.5
        d = 0.001
        clock = 5
        pid = PID(p, i, d)
        pid.SetPoint = 50
        while True:
            feedback = humidity
            pid.update(feedback)
            output = (100 - pid.output) / 100
            pub.sendMessage("actuator.light_status", args=output)  # fan on
            time.sleep(clock)
