from tools.status import Status
from actuator.actuator import Actuator
from pubsub import pub
import RPi.GPIO as GPIO

# Actuator Interface


class Fans(Actuator):
    FAN_IN_PIN0 = 6
    FAN_IN_PIN1 = 13
    FAN_OUT_PIN0 = 19
    FAN_OUT_PIN1 = 26

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
        GPIO.setup(Fans.FAN_IN_PIN0, GPIO.OUT)
        GPIO.setup(Fans.FAN_IN_PIN1, GPIO.OUT)
        GPIO.setup(Fans.FAN_OUT_PIN0, GPIO.OUT)
        GPIO.setup(Fans.FAN_OUT_PIN1, GPIO.OUT)

    def activate(self):
        """activate: sets the current status to Status.ENABLED."""
        self._status = Status.ENABLED

    def actuate(self):
        """actuate: dummy actuation function, to be overriden by children."""
        # TODO DO GPIO OUT BASED ON CURRENT SPEEDS !!
        if (self._fan_in_speed > 0):
            print("fans on!")
            GPIO.output(Fans.FAN_IN_PIN0, GPIO.HIGH)
            GPIO.output(Fans.FAN_IN_PIN1, GPIO.LOW)
        else:
            print("Fans off!")
            GPIO.output(Fans.FAN_IN_PIN0, GPIO.LOW)
            GPIO.output(Fans.FAN_IN_PIN1, GPIO.LOW)
        if (self._fan_out_speed > 0):
            print("fans on!")
            GPIO.output(Fans.FAN_OUT_PIN0, GPIO.HIGH)
            GPIO.output(Fans.FAN_OUT_PIN1, GPIO.LOW)
        else:
            print("Fans off!")
            GPIO.output(Fans.FAN_OUT_PIN0, GPIO.LOW)
            GPIO.output(Fans.FAN_OUT_PIN1, GPIO.LOW)

    def fan_status_listener(self, args, rest=None):
        speed = args
        print("Received speed vals over pubsub:", speed)
        self._fan_out_speed = speed
        self._fan_in_speed = speed
