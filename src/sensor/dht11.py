from seeed_dht import DHT
from pubsub import pub
from sensor.sensor import Sensor
from tools.status import Status
from tools.sensor_data import SensorData
from time import time


class DHT11(Sensor):
    DHT11_PIN = 16

    def __init__(self, *args, **kwargs):
        super().__init__(("humidity", "temperature"), *args, **kwargs)
        self._dht11 = DHT("11", 16)

    def collect(self, pid_update: bool = True):
        self._status = Status.ENABLED
        MODE = "pid_update" if pid_update else "database_update"
        humidity, temp = self._dht11.read()
        # TODO think if magic numbers for sensor type is best option?
        # maybe keep all as enums?
        # (Problematic with mixed type sensors)
        current_t = time()
        pub.sendMessage(
            f"{MODE}.sensor_data.humidity_sensor",
            args=SensorData(current_t, self._id, self._type[0], humidity),
        )
        pub.sendMessage(
            f"{MODE}.sensor_data.ambient_temperature_sensor",
            args=SensorData(current_t, self._id, self._type[1], temp),
        )

    def disable(self):
        self._status = Status.DISABLED
