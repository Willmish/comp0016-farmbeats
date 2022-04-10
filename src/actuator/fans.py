from tools.status import Status
from actuator.actuator import Actuator
from pubsub import pub
import RPi.GPIO as GPIO
from rpi_hardware_pwm import HardwarePWM
from tools.logging import logInfo


class Fans(Actuator):
    #FAN_IN_PIN0 = 6
    #FAN_IN_PIN1 = 13
    #FAN_OUT_PIN0 = 19
    #FAN_OUT_PIN1 = 26
    PWM_CHANNEL = 1
    PWM_FREQUENCY = 50
    FAN_PIN_PWM = 13
    FAN_PIN_SECONDARY = 26
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
        self._fan_speed: int = 0
        self._fan_in_speed: float = 0.0
        self._fan_out_speed: float = 0.0
        pub.subscribe(
            self.fan_status_listener,
            f"{Actuator.MAIN_LISTEN_TOPIC}.actuator.fans_status",
        )
        GPIO.setup(Fans.FAN_PIN_SECONDARY, GPIO.OUT)
        GPIO.output(Fans.FAN_PIN_SECONDARY, GPIO.LOW)
        self._fan_pwm = HardwarePWM(pwm_channel=Fans.PWM_CHANNEL, hz=Fans.PWM_FREQUENCY)
        self._fan_pwm.start(self._fan_speed)
        #GPIO.setup(Fans.FAN_IN_PIN0, GPIO.OUT)
        #GPIO.setup(Fans.FAN_IN_PIN1, GPIO.OUT)
        #GPIO.setup(Fans.FAN_OUT_PIN0, GPIO.OUT)
        #GPIO.setup(Fans.FAN_OUT_PIN1, GPIO.OUT)
        #self._PWM_IN = GPIO.PWM(Fans.FAN_IN_PIN0, 100)
        #self._PWM_OUT = GPIO.PWM(Fans.FAN_OUT_PIN0, 100)
        #self._PWM_IN.start(self._fan_in_speed)
        #self._PWM_OUT.start(self._fan_out_speed)

    def activate(self):
        """activate: sets the current status to Status.ENABLED."""
        self._status = Status.ENABLED

    def actuate(self):
        """actuate: dummy actuation function, to be overriden by children."""
        if self._fan_speed > 20:
            self._fan_pwm.change_duty_cycle(self._fan_speed)
            GPIO.output(Fans.FAN_PIN_SECONDARY, GPIO.LOW)
        else:
            self._fan_pwm.change_duty_cycle(0)
            GPIO.output(Fans.FAN_PIN_SECONDARY, GPIO.LOW)

    def cleanup(self):
        self._fan_pwm.stop()

    def fan_status_listener(self, args, rest=None):
        speed = args.actuator_value
        logInfo(f"Received fan speed value: {speed}%")
        assert 0 <= speed <= 100
        self._fan_speed = speed
        self._fan_out_speed = speed
        self._fan_in_speed = speed
