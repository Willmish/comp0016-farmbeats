from tools.status import Status
from actuator.actuator import Actuator
from pubsub import pub
import RPi.GPIO as GPIO
from rpi_hardware_pwm import HardwarePWM


class LEDLights(Actuator):
    # PWM channel 0 is on PIN 12
    LED_PIN = 12 
    PWM_FREQUENCY = 480
    PWM_CHANNEL = 0

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
        self._brightness: int = 0
        pub.subscribe(
            self.light_status_listener,
            f"{Actuator.MAIN_LISTEN_TOPIC}.actuator.light_status",
        )
        GPIO.setup(LEDLights.LED_PIN, GPIO.OUT)
        self._pwm_light = HardwarePWM(pwm_channel=LEDLights.PWM_CHANNEL, hz=LEDLights.PWM_FREQUENCY)
        self._pwm_light.start(self._brightness)
        #self._PWM_LIGHT = GPIO.PWM(LEDLights.LED_PIN, 490)
        #self._PWM_LIGHT.start(self._brightness)

    def activate(self):
        """activate: sets the current status to Status.ENABLED."""
        self._status = Status.ENABLED

    def actuate(self):
        """actuate: dummy actuation function, to be overriden by children."""
        # Turns LED on and off
        if self._brightness > 0:
            print(f"lights on {self._brightness}%!")
            self._pwm_light.change_duty_cycle(self._brightness)
        else:
            print("lights off!")
            self._pwm_light.change_duty_cycle(0)

    def cleanup(self):
        self._pwm_light.stop()

    def light_status_listener(self, args, rest=None):
        brightness = args.actuator_value
        print("Received brightness vals over pubsub:", brightness)
        self._brightness = brightness
