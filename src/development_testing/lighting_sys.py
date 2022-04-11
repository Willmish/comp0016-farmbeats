from asyncore import read
from random import random
import time
import RPi.GPIO as GPIO
from rpi_hardware_pwm import HardwarePWM
import smbus
import time
import board
import adafruit_bh1750



lights = 5

DEVICE = 0x23 # Default device I2C address
POWER_DOWN = 0x00 # No active state
POWER_ON = 0x01 # Power on
RESET = 0x07 # Reset data register value
ONE_TIME_HIGH_RES_MODE = 0x20

bus = smbus.SMBus(1) # Revision 2 Pi, Pi 2, Pi 3, Pi 4

def convertToNumber(data):
  # Simple function to convert 2 bytes of data
  # into a decimal number
  return ((data[1] + (256 * data[0])) / 1.2)
 
def readLight(addr=DEVICE):
  data = bus.read_i2c_block_data(addr,ONE_TIME_HIGH_RES_MODE)
  time.sleep(0.2)
  return convertToNumber(data)
 
 

def GPIO_output():
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(12, GPIO.OUT)
        GPIO.output(12, GPIO.HIGH)
        print("Lights on!")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Cleaning up!")
        GPIO.cleanup()


# PWM channel is on PIN 12
def PWM_output():
    print(f"Light level: {readLight()} lux")
    pwm = HardwarePWM(pwm_channel=0, hz=480)
    brightness = int(input("Enter PWM output: "))

    pwm.start(brightness) # full duty cycle
    print("Started PWM")
    i2c = board.I2C()
    sensor = adafruit_bh1750.BH1750(i2c)

    try:
        while True:
            print("%.2f Lux"%sensor.lux)
            time.sleep(1)
    except KeyboardInterrupt:
        print("Cleaning up!")
    try:
        while True:
            print(f"lights on {brightness}%!", end="")
            print("Light level: %.2f lux       " % readLight(), end="")
            print("\r", end="")
    except KeyboardInterrupt:
        print("Cleaning up!")
    try:
        while True:
            time.sleep(0.1)
            brightness -= 1
            if brightness < 0:
                brightness = 100
            pwm.change_duty_cycle(brightness)
            print(f"lights on {brightness}%!", end="")
            print("Light level: %.2f lux       " % readLight(), end="")
            print("\r", end="")
    except KeyboardInterrupt:
        print("Cleaning up!")
        pwm.stop()


if __name__ == "__main__":
    PWM_output() 