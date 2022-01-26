from typing import List
from actuator import Actuator


class ActuatorSupervisor:
    def __init__(self):
        self._actuators: List[Actuator] = []

    def add_actuator(self, actuator: Actuator) -> None:
        self._actuators.append(actuator)

