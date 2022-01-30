from seeed_dht import DHT
from pubsub import pub
from sensor.sensor import Sensor 
from tools.status import Status


class DHT11(Sensor):
    DHT11_PIN=16
    def __init__(self, *args, **kwargs):
        super.__init__(("humidity", "temperature"), args, kwargs)
        self._dht11 = DHT("11", 16)

    def collect(self):
        self._status = Status.ENABLED
        humidity, temp = self._dht11.read()
        pub.sendMessage("humidity_sensor", humidity) # TODO send in SensorData object, containing info on the actual sensor
        pub.sendMessage("ambient_temperature_sensor", temp)

    def disable(self):
        self._status = Status.DISABLED


