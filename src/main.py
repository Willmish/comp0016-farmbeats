from json.tool import main
from time import sleep
from actuator.fans import Fans
from actuator.led_lights import LEDLights
from analyser.humidity_analyser import HumidityAnalyser
from analyser.brightness_analyser import BrightnessAnalyser
from analyser.moisture_analyser import WaterAnalyser
from sensor.dht11 import DHT11
from sensor.light_sensor import LightSensor
from sensor.water_level import WaterLevel
from analyser.humidity_pid import HumidityPidAnalyser
from analyser.light_pid import LightPidAnalyser
from analyser.water_pid import MoisturePidAnalyser
from concurrent import futures

# from data_streamer.database_manager import DatabaseManager
from data_streamer.iot_hub_streamer import IoTHubStreamer
from pubsub import pub
import RPi.GPIO as GPIO


TIME_INTERVAL_BETWEEN_READINGS = 5
PID_CLOCK_SPEED = 1


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
        humidity_pid = HumidityPidAnalyser()
        light_pid = LightPidAnalyser()
        water_pid = MoisturePidAnalyser()

        # Sensor DHT11 object
        dht11Sensor = DHT11(sensor_id=1)
        water_level = WaterLevel(sensor_id=2)

        # Light Sensor object
        light_sensor = LightSensor(sensor_id=0)

        # Create Threads
        executor = futures.ThreadPoolExecutor(max_workers=2)

        pub.subscribe(dummy_listener, "humidity_sensor")

        def main_loop():
            try:
                while 1:
                    dht11Sensor.collect(False)  # TODO Move boolean to an Enum
                    light_sensor.collect(False)
                    water_level.collect(False)
                    fans.actuate()
                    # lights.actuate()
                    # print(db)
                    sleep(TIME_INTERVAL_BETWEEN_READINGS)
            except KeyboardInterrupt:
                GPIO.cleanup()
                fans.PWM_cleanup()

        def system_control_loop():
            try:
                while 1:
                    dht11Sensor.collect()  # TODO Move boolean to an Enum
                    light_sensor.collect()
                    water_level.collect()
                    sleep(PID_CLOCK_SPEED)
            except KeyboardInterrupt:
                GPIO.cleanup()

        try:
            while True:
                executor.submit(system_control_loop)
                executor.submit(main_loop)
        except KeyboardInterrupt:
            GPIO.cleanup() # TODO check if necessary
            executor.shutdown()
