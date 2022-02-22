from typing import Union


class SensorData:
    def __init__(self, timestamp: float, sensor_id: int, sensor_type: str,
                 sensor_value: Union[str, int, float]):
        self.timestamp = timestamp
        self.sensor_id = sensor_id
        self.sensor_type = sensor_type
        self.sensor_value = sensor_value

    def __repr__(self):
        return str(self.timestamp) + ' ' + str(self.sensor_id) + ' ' + str(self.sensor_type) + ' ' + str(self.sensor_value)
