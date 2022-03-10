from typing import Union


class SensorData:
    def __init__(
        self,
        timestamp: float,
        sensor_id: int,
        sensor_type: str,
        sensor_value: Union[str, int, float],
        actuator_value: float = None,
    ):
        self.timestamp = timestamp
        self.sensor_id = sensor_id
        self.sensor_type = sensor_type
        self.sensor_value = sensor_value
        self.actuator_value = actuator_value

    def __repr__(self):
        res = "\n"
        res += f"Timestamp: {str(self.timestamp)}\n"
        res += f"Sensor ID: {str(self.sensor_id)}\n"
        res += f"Sensor Type: {str(self.sensor_type)}\n"
        res += f"Value: {str(self.sensor_value)}\n"
        res += f"Actuator Value: {str(self.actuator_value)}\n"
        return res
