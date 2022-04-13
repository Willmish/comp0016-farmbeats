from pubsub import pub
from analyser.analyser import Analyser
from tools.pid import PID
from tools.logging import logCritical, logDebug


class TemperatureAnalyser(Analyser):
    def __init__(self, *args, **kwargs):
        super().__init__(["sensor_data.ambient_temperature_sensor"])
        self._p_parameter = 1.2
        self._i_parameter = 0.5
        self._d_parameter = 0.001
        self._pid = PID(
            self._p_parameter, self._i_parameter, self._d_parameter
        )
        self._pid.SetPoint = 25

    def analyser_listener(self, args, rest=None):
        MAIN_PUBSUB_TOPIC = "pid_update"
        temperature = args.sensor_value
        sensor_data = args
        feedback = temperature
        self._pid.update(feedback)
        output = 100 - self._pid.output  # / 100
        # clamping value to 0-100 range
        output = max(0, min(output, 100))
        sensor_data.actuator_value = output

        if temperature > 35:
            logCritical(
                "Temperature sensor malfunction or system overheating!"
                f"Temperature is {temperature}!"
            )

        logDebug(f"{sensor_data}")
        pub.sendMessage(
            f"{MAIN_PUBSUB_TOPIC}.actuator.heater_status", args=sensor_data
        )

    def datastream_update_listener(self, args, rest=None):
        MAIN_PUBSUB_TOPIC = "database_update"
        temperature = args.sensor_value
        sensor_data = args
        feedback = temperature
        self._pid.update(feedback)
        output = 100 - self._pid.output  # / 100
        # clamping value to 0-100 range
        output = max(0, min(output, 100))
        sensor_data.actuator_value = output

        pub.sendMessage(
            f"{MAIN_PUBSUB_TOPIC}.actuator.heater_status", args=sensor_data
        )
