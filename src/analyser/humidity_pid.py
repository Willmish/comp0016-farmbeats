from pubsub import pub
from analyser.analyser import Analyser
from tools.pid import PID
from tools.logging import logDebug


class HumidityPidAnalyser(Analyser):
    def __init__(self, *args, **kwargs):
        super().__init__(["sensor_data.humidity_sensor"])
        self._p_parameter = 1.2
        self._i_parameter = 0.5
        self._d_parameter = 0.001
        self._pid = PID(
            self._p_parameter,
            self._i_parameter,
            self._d_parameter,
            "./tools/pidHumidityCache",
        )
        self._pid.SetPoint = 65
        self._pid.recover()

    def analyser_listener(self, args, rest=None):
        MAIN_PUBSUB_TOPIC = "pid_update"  # TODO move to enum/config file
        humidity = args.sensor_value
        sensor_data = args
        feedback = humidity
        if humidity < self._pid.SetPoint:
            # prevent PID from decreasing infinitely
            # fans can only decrease humidity
            feedback = self._pid.SetPoint
        self._pid.update(feedback)
        output = 100 - self._pid.output
        # todo need to move this logic somewhere else maybe?
        # clamping value to 0-100 range
        output = int(max(0, min(output, 100)))
        sensor_data.actuator_value = output
        logDebug(f"{sensor_data}")
        pub.sendMessage(
            f"{MAIN_PUBSUB_TOPIC}.actuator.fans_status", args=sensor_data
        )

    def datastream_update_listener(self, args, rest=None):
        MAIN_PUBSUB_TOPIC = "database_update"
        humidity = args.sensor_value
        sensor_data = args
        feedback = humidity
        self._pid.update(feedback)
        output = 100 - self._pid.output
        # todo need to move this logic somewhere else maybe?
        # clamping value to 0-100 range
        output = max(0, min(output, 100))
        sensor_data.actuator_value = output
        self._pid.save()

        pub.sendMessage(
            f"{MAIN_PUBSUB_TOPIC}.actuator.fans_status", args=sensor_data
        )
