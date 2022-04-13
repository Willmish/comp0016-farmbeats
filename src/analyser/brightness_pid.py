from pubsub import pub
from analyser.analyser import Analyser
from tools.pid import PID
from tools.logging import logCritical, logDebug, logWarning, logInfo


class BrightnessPidAnalyser(Analyser):
    def __init__(self, *args, **kwargs):
        super().__init__(["sensor_data.light_sensor"])
        self._p_parameter = 0.05
        self._i_parameter = 0.01
        self._d_parameter = 0.001
        self._pid = PID(
            self._p_parameter, self._i_parameter, self._d_parameter, "./tools/pidLightCache" 
        )
        self._pid.SetPoint = 200
        self._pid.recover()

    def analyser_listener(self, args, rest=None):
        MAIN_PUBSUB_TOPIC = "pid_update"  # TODO move to enum/config file
        brightness = args.sensor_value
        sensor_data = args
        feedback = brightness
        self._pid.update(feedback)
        #logWarning(f"PID output: {self._pid.output}")
        output = self._pid.output
        #logWarning(f"Post-scaling output: {output}")
        # TODO Need to move this logic somewhere else maybe?
        # Clamping value to 0-100 range

        #logWarning(f"PID output: {self._pid.output}")
        #logWarning(f"PID output scaled: {output}")
        output = int(max(0, min(output, 100)))
        

        # TODO SWAP BACK TO OUTPUT ONCE CORRECT SENSOR IN PLACE
        sensor_data.actuator_value = output

        pub.sendMessage(
            f"{MAIN_PUBSUB_TOPIC}.actuator.light_status", args=sensor_data
        )

    def datastream_update_listener(self, args, rest=None):
        MAIN_PUBSUB_TOPIC = "database_update"
        brightness = args.sensor_value
        sensor_data = args
        feedback = brightness
        self._pid.update(feedback)
        output = self._pid.output
        # TODO Need to move this logic somewhere else maybe?
        # Clamping value to 0-100 range
        output = int(max(0, min(output, 100)))

        # TODO SWAP BACK TO OUTPUT ONCE CORRECT SENSOR IN PLACE
        sensor_data.actuator_value = output
        self._pid.save()
        pub.sendMessage(
            f"{MAIN_PUBSUB_TOPIC}.actuator.light_status", args=sensor_data
        )
