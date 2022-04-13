from random import random
import time
import RPi.GPIO as GPIO

pump = 18


def water_sys():
    if if_need_water:
        turn_on()
        time.sleep(10)
        turn_off()


def if_need_water():
    return random(0, 1) > 0.5


def turn_on():
    print("Pump on!")
    GPIO.output(pump, GPIO.HIGH)


def turn_off():
    print("Pump off!")
    GPIO.output(pump, GPIO.LOW)


if __name__ == "__main__":
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pump, GPIO.OUT)
        toggle = False
        while True:
            func = turn_on if toggle else turn_off
            toggle = not toggle
            func()
            time.sleep(1)

    except KeyboardInterrupt:
        print("Cleaning up!")
        GPIO.cleanup()
