from time import time
from pubsub import pub
from sensor.sensor import Sensor
from tools.status import Status
from tools.sensor_data import SensorData


class WaterLevel(Sensor):
    WHATER_LEVEL_PIN = 0

    def __init__(self, *args, **kwargs):
        super().__init__(("waterlevel"), *args, **kwargs)

    def collect(self):
        self._status = Status.ENABLED
        pub.sendMessage(
            "sensor_data.water_level_sensor",
            args=SensorData(
                time(), self._id, self._type
            ),
        )
        # , self.SI1145.ReadUV / 100, self.SI1145.ReadIR)))

    def disable(self):
        self._status = Status.DISABLED
