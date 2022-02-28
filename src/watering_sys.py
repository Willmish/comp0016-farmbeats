from random import random
import time
import RPi.GPIO as GPIO

pump = 0
def water_sys():
    if if_need_water:
        turn_on()
        time.sleep(10)
        turn_off()


def if_need_water():
    return random(0,1)>0.5

def turn_on():
    GPIO.output(pump, GPIO.HIGH)

def turn_off():
    GPIO.output(pump, GPIO.LOW)