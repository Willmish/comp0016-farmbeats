from tools.status import Status
from actuator.actuator import Actuator
# Actuator Interface


class Fans(Actuator):
    FAN_IN_PIN0 = 0
    FAN_IN_PIN1 = 0
    FAN_OUT_PIN0 = 0
    FAN_OUT_PIN1 = 0
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

    def activate(self):
        """activate: sets the current status to Status.ENABLED."""
        self._status = Status.ENABLED

    def actuate(self):
        """actuate: dummy actuation function, to be overriden by children."""
        # TODO DO GPIO OUT BASED ON CURRENT SPEEDS !!
        pass

    def fan_status_listener(self, args, rest=None):
        speed = args
        self._fan_out_speed = speed
        self._fan_in_speed = speed

