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

    def map_number(
        self, val: float, old_max, old_min, new_max, new_min
    ) -> float:
        # try:
        old_range = float(old_max - old_min)
        new_range = float(new_max - new_min)
        new_value = float(((val - old_min) * new_range) / old_range) + new_min
        return new_value
        # except Exception as e:
        #    return val

    def random_generator(self):
        output = random()
        return output
