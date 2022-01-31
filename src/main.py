from time import sleep
from actuator.fans import Fans
from analyser.humidty_analyser import HumidityAnalyser
from sensor.dht11 import DHT11
from pubsub import pub


def dummy_listener(args, rest=None):
    print ("Received message over pubsub:", args)
    

if __name__ == "__main__":
    # Actuator fans object 
    #fans = Fans()

    # Analyser fans object
    #humidity_analyser = HumidityAnalyser()

    # Sensor DHT11 object
    dht11Sensor = DHT11()

    pub.subscribe(dummy_listener, "humidity_sensor")

    while(1):
        dht11Sensor.collect()
        sleep(1)








