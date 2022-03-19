from time import time
from pubsub import pub
from sensor.sensor import Sensor
from tools.status import Status
from tools.sensor_data import SensorData
from grove.adc import ADC


class MoistureSensor(Sensor):
    SOIL_MOISTURE_PIN = 0
    soil_moisture = ADC()

    def __init__(self, *args, **kwargs):
        super().__init__(("soil_moisture"), *args, **kwargs)

    def collect(self, pid_update: bool = True):
        self._status = Status.ENABLED
        MODE = "pid_update" if pid_update else "database_update"
        pub.sendMessage(
            f"{MODE}.sensor_data.soil_moisture_sensor",
            args=SensorData(
                time(),
                self._id,
                self._type,
                self.water_level.read_raw(self.SOIL_MOISTURE_PIN),
            ),
        )

    def disable(self):
        self._status = Status.DISABLED
