from typing import Union


class SensorData:
    def __init__(self, sensor_id: int, sensor_type: str, sensor_value: Union[str, int, float]):
        self.sensor_id = sensor_id
        self.sensor_type = sensor_type
        self.sensor_value = sensor_value
