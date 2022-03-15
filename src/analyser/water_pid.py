from pubsub import pub
from analyser.analyser import Analyser
from pid.pid import PID


class MoisturePidAnalyser(Analyser):
    def __init__(self, *args, **kwargs):
        super().__init__(["sensor_data.soil_moisture_sensor"])

    def analyser_listener(self, args, rest=None):
        print(args.sensor_value)
        soilmoisture = args.sensor_value
        print(soilmoisture)
        p = 1.2
        i = 0.5
        d = 0.001
        pid = PID(p, i, d)
        pid.SetPoint = 50
        voltage = round(((soilmoisture * 3300) / 1024), 0)
        while True:
            feedback = voltage
            pid.update(feedback)
            output = (100 - pid.output) / 100
            pub.sendMessage("actuator.water_pump_status", args=output)
            # percentage time pump needed to be on
