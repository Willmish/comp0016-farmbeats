from time import sleep, time

from sensor.dht11 import DHT11
from analyser.humidity_pid import HumidityPidAnalyser
from actuator.fans import Fans

from sensor.light_sensor import LightSensor
from analyser.brightness_pid import BrightnessPidAnalyser
from actuator.led_lights import LEDLights

from sensor.soil_moisture import SoilMoistureSensor 
from sensor.water_level import WaterLevel
from analyser.water_level_analyser import WaterLevelAnalyser
from actuator.water_pump import WaterPump

from analyser.temperature_analyser import TemperatureAnalyser

from analyser.moisture_analyser import MoisturePidAnalyser

# from data_streamer.database_manager import DatabaseManager
from data_streamer.iot_hub_streamer import IoTHubStreamer
from tools.signal_handler import SignalHandler
import RPi.GPIO as GPIO


TIME_INTERVAL_BETWEEN_READINGS = 5
PID_CLOCK_SPEED = 1


def dummy_listener(args):
    print("Listening all database_update: ", args)


def dummy_listener_pid(args):
    print("Listening all pid_update: ", args)


if __name__ == "__main__":
    singal_handler: SignalHandler = SignalHandler()
    with IoTHubStreamer() as db:
        # db.create_sensor_data_table()
        GPIO.setmode(GPIO.BCM)

        # Actuator objects
        fans = Fans()
        lights = LEDLights()
        water_pump = WaterPump()

        # Analyser objects
        # humidity_analyser = HumidityAnalyser()
        # brightness_analyser = BrightnessAnalyser()
        humidity_pid = HumidityPidAnalyser()
        brightness_pid = BrightnessPidAnalyser()
        #water_level_analyser = WaterLevelAnalyser()
        temperature_analyser = TemperatureAnalyser()
        moisture_analyser = MoisturePidAnalyser()

        # Sensor objects
        light_sensor = LightSensor(sensor_id=0)
        dht11_sensor = DHT11(sensor_id=1)
        water_level = WaterLevel(sensor_id=2)
        moisture_sensor = SoilMoistureSensor(sensor_id=3)

        # pub.subscribe(dummy_listener, "database_update")
        # pub.subscribe(dummy_listener_pid, "pid_update")
        time_since_db_update = time()
        PID_UPDATE = True
        try:
            while 1:
                if (
                    time() - time_since_db_update
                    >= TIME_INTERVAL_BETWEEN_READINGS
                ):
                    print(
                        "++++++++++++++++++++++++++++\n UPDATE DB\n"
                        "++++++++++++++++++++++++++++"
                    )
                    time_since_db_update = time()
                    PID_UPDATE = False
                light_sensor.collect(PID_UPDATE)
                dht11_sensor.collect(PID_UPDATE)
                water_level.collect(PID_UPDATE)
                moisture_sensor.collect(PID_UPDATE)
                fans.actuate()
                lights.actuate()
                #water_pump.actuate()
                PID_UPDATE = True
                sleep(PID_CLOCK_SPEED)

        except KeyboardInterrupt:
            GPIO.cleanup()
