
from seeed_si114x import grove_si114x
import signal
import time
from pubsub import pub
from sensor.sensor import Sensor
from tools.status import Status


class LightSensor(Sensor):
    LIGHT_SENSOR_PIN = 0

    def __init__(self, *args, **kwargs):
        super().__init__(("brightness"), args, kwargs)
        SI1145 = seeed_si114x.grove_si114x()
    
    def handler(signalnum, handler):
        print("Please use Ctrl C to quit")

    def collect(self):
        self._status = Status.ENABLED
        pub.sendMessage("light_sensor", args=(self.SI1145.ReadVisible,
              self.SI1145.ReadUV / 100, self.SI1145.ReadIR))

    def disable(self):
        self._status = Status.DISABLED
