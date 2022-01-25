from Utils.status import Status
# Actuator Interface


class Actuator:
    """Actuator Interface class, to be overriden by actuator subclasses."""

    def __init__(self, actuator_type: str, actuator_id: int, actuator_status: Status = Status.DISABLED):
        """__init__ Initialise an Actuator Interface.

        :param actuator_type:
        :type actuator_type: str
        :param actuator_id:
        :type actuator_id: int
        :param actuator_status:
        :type actuator_status: Status
        """
        self._type: str = actuator_type
        self._id: int = actuator_id
        self._status: Status = actuator_status

    def activate(self):
        """activate: sets the current status to Status.ENABLED."""
        self._status = Status.ENABLED

    def actuate(self):
        """actuate: dummy actuation function, to be overriden by children."""
        pass
