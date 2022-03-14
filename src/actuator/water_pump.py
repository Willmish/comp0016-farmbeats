from tools.status import Status
from actuator.actuator import Actuator
from pubsub import pub
import RPi.GPIO as GPIO


class Waterpump(Actuator):
    PUMP_PIN = 10

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
        pub.subscribe(self.water_pump_listener, f"{Actuator.MAIN_LISTEN_TOPIC}.actuator.pump_status")
        GPIO.setup(Waterpump.PUMP_PIN, GPIO.OUT)

    def activate(self):
        """activate: sets the current status to Status.ENABLED."""
        self._status = Status.ENABLED

    def actuate(self):
        """actuate: dummy actuation function, to be overriden by children."""
        if self._is_on is True:
            print("pump on!")
            GPIO.output(Waterpump.LED_PIN, GPIO.HIGH)
        else:
            print("pump off!")
            GPIO.output(Waterpump.LED_PIN, GPIO.LOW)

    def pump_status_listener(self, args, rest=None):
        status = args
        print("Received pump vals over pubsub:", status)
        self._on = status
