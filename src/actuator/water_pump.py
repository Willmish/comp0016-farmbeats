from tools.sensor_data import SensorData
from tools.status import Status
from actuator.actuator import Actuator
from pubsub import pub
import RPi.GPIO as GPIO


class WaterPump(Actuator):
    PUMP_PIN = 18

    def __init__(self, *args, **kwargs):

        """__init__ Initialise an Actuator Interface.
        :param actuator_type:
        :type actuator_type: str
        :param actuator_id:
        :type actuator_id: int
        :param actuator_status:
        :type actuator_status: Status
        """
        super().__init__("water_pump", args, kwargs)
        self._is_on = True
        pub.subscribe(
            self.water_pump_status_listener,
            f"{Actuator.MAIN_LISTEN_TOPIC}.actuator.water_pump_status",
        )
        GPIO.setup(WaterPump.PUMP_PIN, GPIO.OUT)

    def activate(self):
        """activate: sets the current status to Status.ENABLED."""
        self._status = Status.ENABLED

    def actuate(self):
        """actuate: dummy actuation function, to be overriden by children."""
        if self._is_on is True:
            print("pump on!")
            GPIO.output(WaterPump.PUMP_PIN, GPIO.HIGH)
        else:
            print("pump off!")
            GPIO.output(WaterPump.PUMP_PIN, GPIO.LOW)

    def water_pump_status_listener(self, args: SensorData, rest=None):
        status = args.actuator_value
        print("Received pump vals over pubsub:", status)
        self._is_on = True if status > 0 else False
        self.actuate()
