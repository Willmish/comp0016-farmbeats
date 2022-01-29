from doctest import OutputChecker
from random import random
from Utils.status import Status


class Sensor:

    def __init__(self, sensor_type: str, actuator_id: int, actuator_status: Status = Status.DISABLED):
        self._type: str = sensor_type
        self._id: int = actuator_id
        self._status: Status = actuator_status

    def collect(self):
        self._status = Status.ENABLED
        self.clockspeed = 1

    def sensor(self):
        """dummy one"""
        pass

    def random_generator(self):
        output = random()
        return output
