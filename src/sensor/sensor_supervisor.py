from typing import List
from sensor import Sensor


class SensorSupervisor:
    def __init__(self):
        self._actuators: List[Sensor] = []

    def add_actuator(self, sensor: Sensor) -> None:
        self._actuators.append(sensor)

