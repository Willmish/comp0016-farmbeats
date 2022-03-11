# from pid.humidity_pid import humidity_pid_control
from pubsub import pub
from analyser.analyser import Analyser
from pid.pid import PID
import time


class HumidityAnalyser(Analyser):
    def __init__(self, *args, **kwargs):
        super().__init__(["sensor_data.humidity_sensor"])

    def analyser_listener(self, args, rest=None):
        sensor_data = args
        humidity = args.sensor_value
        # TODO Do analysing stuff here, currently simple threshold
        if humidity > 80:
            sensor_data.actuator_value = 100
            pub.sendMessage(
                "actuator.fans_status", args=sensor_data
            )  # Fans 50% on
        elif humidity > 70:
            sensor_data.actuator_value = 70
            pub.sendMessage(
                "actuator.fans_status", args=sensor_data
            )  # Fans 20% on
        else:
            sensor_data.actuator_value = 0
            pub.sendMessage("actuator.fans_status", args=sensor_data)
            # FailsafeDefault value (for safety reasons,
            # keep it as 0, as per our security module :)

    def pid_control(self, args, temprature, clock):
        p = 1.2
        i = 0.5
        d = 0.001
        pid = PID(p, i, d)
        pid.SetPoint = temprature
        while True:
            feedback = args.sensor_value
            pid.update(feedback)
            output = 100 - pid.output
            pub.sendMessage("actuator.fans_status", args=output)
            time.sleep(clock)
