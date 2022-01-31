from tools.status import Status
from actuator.actuator import Actuator
from pubsub import pub
import RPi.GPIO as GPIO

# Actuator Interface


class Fans(Actuator):
    FAN_IN_PIN0 = 31
    FAN_IN_PIN1 = 33
    FAN_OUT_PIN0 = 35
    FAN_OUT_PIN1 = 37

    def __init__(self, *args, **kwargs):
        """__init__ Initialise an Actuator Interface.

        :param actuator_type:
        :type actuator_type: str
        :param actuator_id:
        :type actuator_id: int
        :param actuator_status:
        :type actuator_status: Status
        """
        super().__init__("fans", args, kwargs)
        self._fan_in_speed: float = .0
        self._fan_out_speed: float = .0
        pub.subscribe(self.fan_status_listener, "fans_status")
        GPIO.setup(31, GPIO.OUT)
        GPIO.setup(33, GPIO.OUT)
        GPIO.setup(35, GPIO.OUT)
        GPIO.setup(37, GPIO.OUT)

    def activate(self):
        """activate: sets the current status to Status.ENABLED."""
        self._status = Status.ENABLED

    def actuate(self):
        """actuate: dummy actuation function, to be overriden by children."""
        # TODO DO GPIO OUT BASED ON CURRENT SPEEDS !!
        if (self._fan_in_speed > 0):
            pass
        if (self._fan_out_speed >0):
            GPIO.output(35, GPIO.HIGH)
            GPIO.output(37, GPIO.LOW)
        else:
            GPIO.output(35, GPIO.LOW)
            GPIO.output(37, GPIO.LOW)

    def fan_status_listener(self, args, rest=None):
        speed = args
        self._fan_out_speed = speed
        self._fan_in_speed = speed
