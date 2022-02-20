from seeed_si114x import grove_si114x
from time import time
from pubsub import pub
from sensor.sensor import Sensor
from tools.status import Status
from tools.sensor_data import SensorData


class LightSensor(Sensor):
    LIGHT_SENSOR_PIN = 0

    def __init__(self, *args, **kwargs):
        super().__init__(("brightness"), args, kwargs)
        self.SI1145 = grove_si114x()

    def collect(self):
        self._status = Status.ENABLED
        pub.sendMessage("sensor_data.light_sensor", args=SensorData(time(),
                        self._id, self._type[0], (self.SI1145.ReadVisible,
                        self.SI1145.ReadUV / 100, self.SI1145.ReadIR)))

    def disable(self):
        self._status = Status.DISABLED
