from time import sleep
from actuator.fans import Fans
from actuator.led_lights import LEDLights
from analyser.humidty_analyser import HumidityAnalyser
from analyser.brightness_analyser import BrightnessAnalyser
from analyser.moisture_analyser import WaterAnalyser
from sensor.dht11 import DHT11
from sensor.light_sensor import LightSensor
from sensor.water_level import WaterLevel

# from database.database_manager import DatabaseManager
from database.iot_hub_streamer import IoTHubStreamer
from pubsub import pub
import RPi.GPIO as GPIO


TIME_INTERVAL_BETWEEN_READINGS = 5


def dummy_listener(args, rest=None):
    print("Received message over pubsub:", args.sensor_value)


if __name__ == "__main__":
    with IoTHubStreamer() as db:
        # db.create_sensor_data_table()
        GPIO.setmode(GPIO.BCM)
        # Actuator fans object
        fans = Fans()
        lights = LEDLights()

        # Analyser fans object
        humidity_analyser = HumidityAnalyser()
        brightness_analyser = BrightnessAnalyser()
        water_analyser = WaterAnalyser()

        # Sensor DHT11 object
        dht11Sensor = DHT11(sensor_id=1)
        water_level = WaterLevel(sensor_id=2)

        # Light Sensor object
        light_sensor = LightSensor(sensor_id=0)

        pub.subscribe(dummy_listener, "humidity_sensor")
        try:
            while 1:
                dht11Sensor.collect()
                light_sensor.collect()
                water_level.collect()
                fans.actuate()
                # lights.actuate()
                # print(db)
                sleep(TIME_INTERVAL_BETWEEN_READINGS)
        except KeyboardInterrupt:
            GPIO.cleanup()
            fans.PWM_cleanup()
