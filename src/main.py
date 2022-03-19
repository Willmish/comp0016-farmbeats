from time import sleep

from sensor.dht11 import DHT11
from analyser.humidity_analyser import HumidityAnalyser
from analyser.humidity_pid import HumidityPidAnalyser
from actuator.fans import Fans

from sensor.light_sensor import LightSensor
from analyser.brightness_analyser import BrightnessAnalyser
from analyser.light_pid import LightPidAnalyser
from actuator.led_lights import LEDLights

#from sensor.soil_moisture import MoistureSensor
#from sensor.water_level import WaterLevel
#from analyser.moisture_analyser import MoistureAnalyser 
#from analyser.water_pid import MoisturePidAnalyser


from concurrent import futures

# from data_streamer.database_manager import DatabaseManager
from data_streamer.iot_hub_streamer import IoTHubStreamer
from pubsub import pub
import RPi.GPIO as GPIO


TIME_INTERVAL_BETWEEN_READINGS = 5
PID_CLOCK_SPEED = 1

def dummy_listener(args):
    print("Listening all database_update: " , args)

def dummy_listener_pid(args):
    print("Listening all pid_update: " , args)

if __name__ == "__main__":
    with IoTHubStreamer() as db:
        # db.create_sensor_data_table()
        GPIO.setmode(GPIO.BCM)

        # Actuator fans object
        fans = Fans()
        lights = LEDLights()

        # Analyser fans object
        #humidity_analyser = HumidityAnalyser()
        #brightness_analyser = BrightnessAnalyser()
        humidity_pid = HumidityPidAnalyser()
        light_pid = LightPidAnalyser()
        #water_pid = MoisturePidAnalyser()

        # Sensor DHT11 object
        dht11Sensor = DHT11(sensor_id=1)
        #water_level = WaterLevel(sensor_id=2)

        # Light Sensor object
        light_sensor = LightSensor(sensor_id=0)

        # Create Threads
        executor = futures.ThreadPoolExecutor(max_workers=2)

        #pub.subscribe(dummy_listener, "database_update")
        #pub.subscribe(dummy_listener_pid, "pid_update")
        def main_loop():
            try:
                while 1:
                    dht11Sensor.collect(False)  # TODO Move boolean to an Enum
                    light_sensor.collect(False)
                    #water_level.collect(False)
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
                    fans.actuate()
                    #water_level.collect()
                    sleep(PID_CLOCK_SPEED)
            except KeyboardInterrupt:
                GPIO.cleanup()

        try:
            system_control_loop()
            #main_loop()
            #while True:
            #    #executor.submit(system_control_loop)
            #    executor.submit(main_loop)
        except KeyboardInterrupt:
            GPIO.cleanup() # TODO check if necessary
            executor.shutdown()
