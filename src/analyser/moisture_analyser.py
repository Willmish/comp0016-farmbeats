from pubsub import pub
from analyser.analyser import Analyser
from pid.pid import PID
import time
import tools.config as config

class MoisturePidAnalyser(Analyser):
    def __init__(self, *args, **kwargs):
        super().__init__([config.sensor_data + "." + config.soil_moisture_sensor])
        self._p_parameter = 1.2
        self._i_parameter = 0.5
        self._d_parameter = 0.001
        self._pid = PID(
            self._p_parameter, self._i_parameter, self._d_parameter
        )
        self._pid.SetPoint = 50

    def analyser_listener(self, args, rest=None):
        MAIN_PUBSUB_TOPIC = config.pid_update  # TODO move to enum/config file
        soilmoisture = round(((args.sensor_value * 3300) / 1024), 0)
        sensor_data = args
        feedback = soilmoisture
        self._pid.update(feedback)
        output = (100 - self._pid.output) / 100
        sensor_data.actuator_value = output

        # TODO change so can work asynchronously (clock needs to be passed from
        # outside loop, actuator has to be working asynchronously and
        # monitor/on/off state)
        clock = 5
        pub.sendMessage(
            f"{MAIN_PUBSUB_TOPIC}.{config.actuator}.{config.water_pump_status}", args=1.0
        )  # pump on
        time.sleep(output * clock)
        pub.sendMessage(
            f"{MAIN_PUBSUB_TOPIC}.{config.actuator}.{config.water_pump_status}", args=0
        )  # pump off
        time.sleep(clock - (output * clock))

    def datastream_update_listener(self, args, rest=None):
        MAIN_PUBSUB_TOPIC = config.database_update
        sensor_data = args
        output = (100 - self._pid.output) / 100
        sensor_data.actuator_value = output
        # TODO either change to send the on off status (will be inaccurate)
        # , or see issue #55
        pub.sendMessage(
            f"{MAIN_PUBSUB_TOPIC}.{config.actuator}.{config.water_pump_status}", args=sensor_data
        )
