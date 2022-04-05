from pubsub import pub
from analyser.analyser import Analyser
from pid.pid import PID
import tools.config as config
from tools.analysis_constants import Analysis_Constants as analysis


class HumidityPidAnalyser(Analyser):
    def __init__(self, *args, **kwargs):
        super().__init__([config.sensor_data + "." + config.humidity_sensor])
        self._p_parameter = analysis.HUMIDITY_P
        self._i_parameter = analysis.HUMIDITY_I
        self._d_parameter = analysis.HUMIDITY_D
        self._pid = PID(
            self._p_parameter, self._i_parameter, self._d_parameter
        )
        self._pid.SetPoint = analysis.HUMIDITY_SETPOINT

    def analyser_listener(self, args, rest=None):
        MAIN_PUBSUB_TOPIC = config.pid_update # TODO move to enum/config file
        humidity = args.sensor_value
        sensor_data = args
        feedback = humidity
        self._pid.update(feedback)
        output = 100 - self._pid.output  # / 100
        # todo need to move this logic somewhere else maybe?
        # clamping value to 0-100 range
        output = max(0, min(output, 100))
        sensor_data.actuator_value = output

        pub.sendMessage(
            f"{MAIN_PUBSUB_TOPIC}.{config.actuator}.{config.fans_status}", args=sensor_data
        )

    def datastream_update_listener(self, args, rest=None):
        MAIN_PUBSUB_TOPIC = config.database_update
        humidity = args.sensor_value
        sensor_data = args
        feedback = humidity
        self._pid.update(feedback)
        output = 100 - self._pid.output  # / 100
        # todo need to move this logic somewhere else maybe?
        # clamping value to 0-100 range
        output = max(0, min(output, 100))
        sensor_data.actuator_value = output

        print("DB update: ", sensor_data)
        pub.sendMessage(
            f"{MAIN_PUBSUB_TOPIC}.{config.actuator}.{config.fans_status}", args=sensor_data
        )
