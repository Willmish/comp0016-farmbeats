from typing import List
from sensor import sensor


class sensorSupervisor:
    def __init__(self):
        self._actuators: List[sensor] = []

    def add_actuator(self, sensor: sensor) -> None:
        self._actuators.append(sensor)

