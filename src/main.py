from time import sleep
from actuator.fans import Fans
from analyser.humidty_analyser import HumidityAnalyser
from sensor.dht11 import DHT11
from database.database_manager import DatabaseManager
from pubsub import pub
import RPi.GPIO as GPIO


def dummy_listener(args, rest=None):
    print("Received message over pubsub:", args)


if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    # Actuator fans object
    fans = Fans()

    # Analyser fans object
    humidity_analyser = HumidityAnalyser()

    # Sensor DHT11 object
    dht11Sensor = DHT11()

    pub.subscribe(dummy_listener, "humidity_sensor")

    try:
        while(1):
            dht11Sensor.collect()
            fans.actuate()
            sleep(1)
    except KeyboardInterrupt:
        GPIO.cleanup()
        #fans.PWM_cleanup()
