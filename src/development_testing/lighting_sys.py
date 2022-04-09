from random import random
import time
import RPi.GPIO as GPIO
from rpi_hardware_pwm import HardwarePWM


lights = 5



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
    try:
        pwm = HardwarePWM(pwm_channel=0, hz=480)
        brightness = 100
        pwm.start(100) # full duty cycle
        print("Started PWM")
        time.sleep(5)
        print(f"lights on {brightness}%!")
        while True:
            time.sleep(0.1)
            brightness -= 1
            if brightness < 0:
                brightness = 100
            pwm.change_duty_cycle(brightness)
            print(f"lights on {brightness}%!")
    except KeyboardInterrupt:
        print("Cleaning up!")
        pwm.stop()


if __name__ == "__main__":
    PWM_output() 