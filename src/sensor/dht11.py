from seeed_dht import DHT
from pubsub import pub
from sensor.sensor import Sensor
from tools.status import Status
from tools.sensor_data import SensorData
from time import time
import tools.config

class DHT11(Sensor):
    DHT11_PIN = 16

    def __init__(self, *args, **kwargs):
        super().__init__(("humidity", "temperature"), *args, **kwargs)
        self._dht11 = DHT("11", 16)

    def collect(self):
        self._status = Status.ENABLED
        humidity, temp = self._dht11.read()
        # TODO think if magic numbers for sensor type is best option?
        # maybe keep all as enums?
        # (Problematic with mixed type sensors)
        pub.sendMessage(
            tools.config.sensor['humidity_sensor'],
            args=SensorData(time(), self._id, self._type[0], humidity),
        )
        pub.sendMessage(
            tools.config.sensor['temperature_sensor'],
            args=SensorData(time(), self._id, self._type[1], temp),
        )

    def disable(self):
        self._status = Status.DISABLED
