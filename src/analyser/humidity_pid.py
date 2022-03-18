from pubsub import pub
from analyser.analyser import Analyser
from pid.pid import PID
import time
import tools.config

class HumidityPidAnalyser(Analyser):
    def __init__(self, *args, **kwargs):
        super().__init__(["sensor_data.humidity_sensor"])

    def analyser_listener(self, args, rest=None):
        humidity = args.sensor_value
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
            pub.sendMessage(tools.config.status['light_status'], args=output)
            time.sleep(clock)
