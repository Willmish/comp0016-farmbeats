from tools.status import Status
from actuator.actuator import Actuator
from pubsub import pub
import RPi.GPIO as GPIO

# Actuator Interface


class LEDLights(Actuator):
    LED_PIN = 5

    def __init__(self, *args, **kwargs):
        
        """__init__ Initialise an Actuator Interface.
        :param actuator_type:
        :type actuator_type: str
        :param actuator_id:
        :type actuator_id: int
        :param actuator_status:
        :type actuator_status: Status
        """
        super().__init__("led_lights", args, kwargs)
        self._brightness = 0
        pub.subscribe(self.light_status_listener, "light_status")
        GPIO.setup(LEDLights.LED_PIN, GPIO.OUT)
        

    def activate(self):
        """activate: sets the current status to Status.ENABLED."""
        self._status = Status.ENABLED

    def actuate(self):
        """actuate: dummy actuation function, to be overriden by children."""
        # Turns LED on and off
        if (self._brightness > 0):
            print("lights on!")
            GPIO.output(LEDLights.LED_PIN, GPIO.HIGH)
        else:
            print("lights off!")
            GPIO.output(LEDLights.LED_PIN, GPIO.LOW)
        

    def light_status_listener(self, args, rest=None):
        brightness = args
        print("Received brightness vals over pubsub:", brightness)
        self._brightness = brightness
