from pubsub import pub
from analyser.analyser import Analyser
from pid.pid import PID
import time


class HumidityPidAnalyser(Analyser):
    def __init__(self, *args, **kwargs):
        super().__init__(["sensor_data.humidity_sensor"])
        self._p_parameter = 1.2
        self._i_parameter = 0.5
        self._d_parameter = 0.001
        self._pid = PID(self._p_parameter, self._i_parameter, self._d_parameter)
        self._pid.SetPoint = 50

    def analyser_listener(self, args, rest=None):
        MAIN_PUBSUB_TOPIC = "pid_update"  # TODO move to enum/config file
        humidity = args.sensor_value
        sensor_data = args
        feedback = humidity
        self._pid.update(feedback)
        output = (100 - self._pid.output) / 100
        sensor_data.actuator_value = output

        pub.sendMessage(f"{MAIN_PUBSUB_TOPIC}.actuator.fans_status", args=sensor_data)

    def analyser_datastream_update_listener(self, args, rest=None):
        MAIN_PUBSUB_TOPIC = "database_update"
        sensor_data = args
        output = (100 - self._pid.output) / 100
        sensor_data.actuator_value = output
        pub.sendMessage(f"{MAIN_PUBSUB_TOPIC}.actuator.fans_status", args=sensor_data)
