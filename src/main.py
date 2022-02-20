from time import sleep
from actuator.fans import Fans
from actuator.led_lights import LEDLights
from analyser.humidty_analyser import HumidityAnalyser
from analyser.brightness_analyser import BrightnessAnalyser
from sensor.dht11 import DHT11
from sensor.light_sensor import LightSensor
from database.database_manager import DatabaseManager
from pubsub import pub
import RPi.GPIO as GPIO


def dummy_listener(args, rest=None):
    print("Received message over pubsub:", args.sensor_value)


if __name__ == "__main__":
    db = DatabaseManager()
    db.connect()
    db.create_sensor_data_table()
    GPIO.setmode(GPIO.BCM)
    # Actuator fans object
    fans = Fans()
    lights = LEDLights()

    # Analyser fans object
    humidity_analyser = HumidityAnalyser()
    brightness_analyser = BrightnessAnalyser()

    # Sensor DHT11 object
    dht11Sensor = DHT11()

    # Light Sensor object
    light_sensor = LightSensor()

    pub.subscribe(dummy_listener, "humidity_sensor")
    try:
        while(1):
            dht11Sensor.collect()
            light_sensor.collect()
            fans.actuate()
            lights.actuate()
            sleep(1)
    except KeyboardInterrupt:
        GPIO.cleanup()
        fans.PWM_cleanup()
