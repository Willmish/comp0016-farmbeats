from time import time
from pubsub import pub
from sensor.sensor import Sensor
from tools.status import Status
from tools.sensor_data import SensorData
from grove.adc import ADC


class WaterLevel(Sensor):
    WATER_LEVEL_PIN = 2
    water_level = ADC()
    
    def __init__(self, *args, **kwargs):
        super().__init__(("waterlevel"), *args, **kwargs)

    def collect(self):
        self._status = Status.ENABLED
        pub.sendMessage(
            "sensor_data.water_level_sensor",
            args=SensorData(
                time(), self._id, self._type, 
                self.water_level.read_raw(self.WATER_LEVEL_PIN)
            ),
        )

    def disable(self):
        self._status = Status.DISABLED
