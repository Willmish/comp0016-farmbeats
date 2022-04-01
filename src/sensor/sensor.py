from random import random
from typing import Tuple
from tools.status import Status


class Sensor:
    def __init__(
        self,
        sensor_type: Tuple[str, ...],
        sensor_id: int,
        sensor_status: Status = Status.DISABLED,
    ):
        self._type: str = sensor_type
        self._id: int = sensor_id
        self._status: Status = sensor_status

    def collect(self, pid_update: bool = True):
        self._status = Status.ENABLED
        self.clockspeed = 1

    def random_generator(self):
        output = random()
        return output
