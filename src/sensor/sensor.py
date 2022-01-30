from doctest import OutputChecker
from random import random
from typing import Tuple
from tools.status import Status


class Sensor:

    def __init__(self, sensor_type: Tuple[str, ...], sensor_id: int, sensor_status: Status = Status.DISABLED):
        self._type: str = sensor_type
        self._id: int =sensor_id 
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
