#!/usr/bin/env python3
import time
from seeed_dht import DHT
from seeed_si114x import grove_si114x
from grove.adc import ADC
import signal
from rpi_hardware_pwm import HardwarePWM


def handler(signalnum, handler):
    print("Use Ctrl C to quit")
    # Using SIGSTP of SIGQUIT messes up i2c reading

def map_number(val: float, old_max, old_min, new_max, new_min) -> float:
    #try:
    old_range = float(old_max - old_min)
    new_range = float(new_max - new_min)
    new_value = float(((val - old_min) * new_range) / old_range) + new_min
    return new_value

def PWM_output():
    try:
        pwm = HardwarePWM(pwm_channel=0, hz=480)
        brightness = 0
        pwm.start(brightness) # full duty cycle
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



def main():
    print("Use Ctrl C to quit")
    signal.signal(signal.SIGTSTP, handler)  # Ctrl-z
    signal.signal(signal.SIGQUIT, handler)  # Ctrl-\
    # for DHT11/DHT22
    dht = DHT("11", 16)
    SI1145 = grove_si114x()
    soil_sensor_pin = 0
    soil_sensor = ADC()
    water_level_pin = 2
    water_level = ADC()
    # for DHT10
    # sensor = seeed_dht.DHT("10")
    pwm = HardwarePWM(pwm_channel=0, hz=480)
    brightness = 30
    pwm.start(brightness) # full duty cycle

    try:
        while True:
            pwm.change_duty_cycle(brightness)
            humi, temp = dht.read()
            if humi is not None:
                print(
                    "DHT{0}, humidity {1:.1f}%, temperature {2:.1f}*".format(
                        dht.dht_type, humi, temp
                    ),
                    end=" ",
                )
            else:
                print(
                    "DHT{0}, humidity & temperature: {1}".format(
                        dht.dht_type, temp
                    ),
                    end=" ",
                )
            print(
                "Visible %.2f UV %.2f IR %03d"
                % (SI1145.ReadVisible, SI1145.ReadUV / 100, SI1145.ReadIR),
                end=" ",
            )
            print(
                f"Soil humdity: {soil_sensor.read_raw(soil_sensor_pin)}", end=" "
            )
            print(f"Brightness: {brightness}%", end=" ")
            print(
                f"Water level raw: {water_level.read_raw(water_level_pin)}", end=" "
            )
            print(
                f"Water level: {map_number(water_level.read_raw(water_level_pin), 2100, 250, 100, 0)}", end=" "
            )
            #brightness -= 10
            #if brightness < 0:
            #    brightness = 100
            
            print("\n", end="")
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Cleaning up!")
        pwm.stop()


if __name__ == "__main__":
    main()
