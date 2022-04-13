from time import time, sleep
from pubsub import pub
import smbus
from sensor.sensor import Sensor
from tools.exceptions import SensorException
from tools.logging import logWarning
from tools.status import Status
from tools.sensor_data import SensorData


class LightSensor(Sensor):
    LIGHT_SENSOR_PIN = 0
    DEVICE = 0x23  # Default device I2C address
    POWER_DOWN = 0x00  # No active state
    POWER_ON = 0x01  # Power on
    RESET = 0x07  # Reset data register value
    ONE_TIME_HIGH_RES_MODE = 0x20

    def __init__(self, *args, **kwargs):
        super().__init__(("brightness"), *args, **kwargs)
        self._i2c_bus = smbus.SMBus(1)  # Revision 2 Pis use 1

    def get_lux_value(self, addr=DEVICE):
        attempt: int = 0
        while True:
            try:
                raw_data: bytes = self._i2c_bus.read_i2c_block_data(
                    addr, LightSensor.ONE_TIME_HIGH_RES_MODE
                )
                break
            except IOError:
                logWarning(
                    f"IOError: Could not read from I2C bus, attempt {attempt}"
                )
                if attempt >= 10:
                    raise SensorException(
                        "LightSensor: Could not read from I2C bus"
                    )
                attempt += 1
                sleep(0.1)
        return self.convert_to_lux(raw_data)

    def convert_to_lux(self, data):
        return (data[1] + (256 * data[0])) / 1.2

    def collect(self, pid_update: bool = True):
        self._status = Status.ENABLED
        MODE = "pid_update" if pid_update else "database_update"
        pub.sendMessage(
            f"{MODE}.sensor_data.light_sensor",
            args=SensorData(
                time(), self._id, self._type, (self.get_lux_value())
            ),
        )

    def disable(self):
        self._status = Status.DISABLED
