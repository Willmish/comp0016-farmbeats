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
        pub.subscribe(self.fan_status_listener, "actuator.fans_status")
        GPIO.setup(Fans.FAN_IN_PIN0, GPIO.OUT)
        GPIO.setup(Fans.FAN_IN_PIN1, GPIO.OUT)
        GPIO.setup(Fans.FAN_OUT_PIN0, GPIO.OUT)
        GPIO.setup(Fans.FAN_OUT_PIN1, GPIO.OUT)
        # self._PWM_IN = GPIO.PWM(Fans.FAN_IN_PIN0, 200)
        # self._PWM_OUT = GPIO.PWM(Fans.FAN_OUT_PIN0, 200)
        # self._PWM_IN.start(self._fan_in_speed)
        # self._PWM_OUT.start(self._fan_out_speed)

    def activate(self):
        """activate: sets the current status to Status.ENABLED."""
        self._status = Status.ENABLED

    def actuate(self):
        """actuate: dummy actuation function, to be overriden by children."""
        # TODO DO GPIO OUT BASED ON CURRENT SPEEDS !!
        # MAKE SURE PWM IS IN BETWEEN 0 and 100 (%)
        if (self._fan_in_speed > 0):
            print("fans in on!")
            # self._PWM_IN.ChangeDutyCycle(self._fan_in_speed)
            GPIO.output(Fans.FAN_IN_PIN1, GPIO.LOW)
            GPIO.output(Fans.FAN_IN_PIN0, GPIO.HIGH)
            # for i in range(100, 0, -10):
            #    self._fan_in_speed = i
            #    self._PWM_IN.ChangeDutyCycle(self._fan_in_speed)
            #    GPIO.output(Fans.FAN_IN_PIN1, GPIO.LOW)
            #    print("spinning in, speed: ", i)
            #    sleep(2)
        else:
            print("Fans in off!")
            GPIO.output(Fans.FAN_IN_PIN0, GPIO.LOW)
            # self._PWM_IN.ChangeDutyCycle(self._fan_in_speed)
            GPIO.output(Fans.FAN_IN_PIN1, GPIO.LOW)
        if (self._fan_out_speed > 0):
            print("fans out on!")
            # self._PWM_OUT.ChangeDutyCycle(self._fan_out_speed)
            GPIO.output(Fans.FAN_OUT_PIN0, GPIO.HIGH)
            GPIO.output(Fans.FAN_OUT_PIN1, GPIO.LOW)
            # for i in range(100, 0, -10):
            #    self._fan_out_speed = i
            #    #GPIO.output(Fans.FAN_OUT_PIN0, GPIO.HIGH)
            #    self._PWM_OUT.ChangeDutyCycle(self._fan_out_speed)
            #    GPIO.output(Fans.FAN_OUT_PIN1, GPIO.LOW)
            #    print("spinning out, speed: ", i)
            #    sleep(0.5)
        else:
            print("Fans out off!")
            GPIO.output(Fans.FAN_OUT_PIN0, GPIO.LOW)
            # self._PWM_OUT.ChangeDutyCycle(self._fan_out_speed)
            GPIO.output(Fans.FAN_OUT_PIN1, GPIO.LOW)

    def PWM_cleanup(self):
        self._PWM_IN.stop()
        self._PWM_OUT.stop()

    def fan_status_listener(self, args, rest=None):
        speed = args
        print("Received speed vals over pubsub:", speed)
        assert(0 <= speed <= 100)
        self._fan_out_speed = speed
        self._fan_in_speed = speed
