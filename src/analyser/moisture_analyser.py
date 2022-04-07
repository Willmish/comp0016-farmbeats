from pubsub import pub
from analyser.analyser import Analyser
from pid.pid import PID
import time


class MoisturePidAnalyser(Analyser):
    MIN_WATER_LEVEL: float = 10.0
    POURING_TIME: float = 5.0
    SOAKING_IN_TIME: float = 10.0
    TARGET_MOISTURE_LEVEL: float = 30.0
    MAX_DRYNESS_DEVIATION : float = 1.0
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(["sensor_data.soil_moisture_sensor", "sensor_data.water_level_sensor"])
        self._p_parameter = 1.2
        self._i_parameter = 0.5
        self._d_parameter = 0.001
        self._pid = PID(
            self._p_parameter, self._i_parameter, self._d_parameter
        )
        self._pid.SetPoint = 50
        self._last_water_level = None
        self._last_time_poured = time.time() - MoisturePidAnalyser.SOAKING_IN_TIME

    def analyser_listener(self, args, rest=None) -> None:
        if args.sensor_type == "water_level":
            self.water_level_handler(args)
        else:
            if self._last_water_level is not None:
                # If the system managed to read the last water level,
                # allow for control of pumps (water level status known)
                self.soil_moisture_handler(args)
        

    def datastream_update_listener(self, args, rest=None) -> None:
        if args.sensor_type == "water_level":
            self.water_level_datastream_update_handler(args)
        else:
            if self._last_water_level is not None:
                # If the system managed to read the last water level,
                # allow for control of pumps (water level status known)
                self.soil_moisture_datastream_update_handler(args)
        

    def water_level_handler(self, args) -> None:
        MAIN_PUBSUB_TOPIC = "pid_update"
        # 670-2100
        sensor_data = args
        self._last_water_level = sensor_data.sensor_value
        # TODO consider changing this structure, as it has no actuator!
        sensor_data.actuator_value = (
            -1
        )  # Set actuator to -1 to avoid null values in DB
        pub.sendMessage(
            f"{MAIN_PUBSUB_TOPIC}.actuator.water_level", args=sensor_data
        )

    def water_level_datastream_update_handler(self, args) -> None:
        MAIN_PUBSUB_TOPIC = "database_update"
        sensor_data = args
        self._last_water_level = sensor_data.sensor_value
        sensor_data.actuator_value = -1
        pub.sendMessage(
            f"{MAIN_PUBSUB_TOPIC}.actuator.water_level", args=sensor_data
        )

    def soil_moisture_handler(self, args) -> None:
        MAIN_PUBSUB_TOPIC = "pid_update"  # TODO move to enum/config file
        if self._last_water_level < MoisturePidAnalyser.MIN_WATER_LEVEL:
            print("Water level in the tank too low to pump water!")
            return

        soil_moisture = args.sensor_value
        sensor_data = args
        #self._pid.update(soil_moisture)
        #output = (100 - self._pid.output) / 100
        #sensor_data.actuator_value = output

        # TODO change so can work asynchronously (clock needs to be passed from
        # outside loop, actuator has to be working asynchronously and
        # monitor/on/off state)
        if (MoisturePidAnalyser.TARGET_MOISTURE_LEVEL - soil_moisture >= MoisturePidAnalyser.MAX_DRYNESS_DEVIATION):
            if (time.time() - self._last_time_poured >= MoisturePidAnalyser.SOAKING_IN_TIME):
                self._last_time_poured = time.time()
                pub.sendMessage(
                    f"{MAIN_PUBSUB_TOPIC}.actuator.water_pump_status", args=1.0
                )  # pump on
                time.sleep(MoisturePidAnalyser.POURING_TIME)
                pub.sendMessage(
                    f"{MAIN_PUBSUB_TOPIC}.actuator.water_pump_status", args=0.0
                )  # pump off



    def soil_moisture_datastream_update_handler(self, args):
        MAIN_PUBSUB_TOPIC = "database_update"
        if self._last_water_level < MoisturePidAnalyser.MIN_WATER_LEVEL:
            print("Water level in the tank too low to pump water!")
            return
        soil_moisture = args.sensor_value
        sensor_data = args
        #output = (100 - self._pid.output) / 100
        sensor_data.actuator_value = 0.0
        if (MoisturePidAnalyser.TARGET_MOISTURE_LEVEL - soil_moisture >= MoisturePidAnalyser.MAX_DRYNESS_DEVIATION):
            if (time.time() - self._last_time_poured >= MoisturePidAnalyser.SOAKING_IN_TIME):
                sensor_data.actuator_value = 1.0 
        # TODO either change to send the on off status (will be inaccurate)
        # , or see issue #55
        pub.sendMessage(
            f"{MAIN_PUBSUB_TOPIC}.actuator.water_pump_status", args=sensor_data
        )