#!/usr/bin/env python3
import time
from seeed_dht import DHT
from seeed_si114x import grove_si114x
from grove.adc import ADC
import signal


def handler(signalnum, handler):
    print("Use Ctrl C to quit")
    # Using SIGSTP of SIGQUIT messes up i2c reading


def main():
    print("Use Ctrl C to quit")
    signal.signal(signal.SIGTSTP, handler)  # Ctrl-z
    signal.signal(signal.SIGQUIT, handler)  # Ctrl-\
    # for DHT11/DHT22
    dht = DHT("11", 16)
    SI1145 = grove_si114x()
    soil_sensor_pin = 0
    soil_sensor = ADC()
    # for DHT10
    # sensor = seeed_dht.DHT("10")

    while True:
        humi, temp = dht.read()
        if humi is not None:
            print('DHT{0}, humidity {1:.1f}%, temperature {2:.1f}*'.format(
                  dht.dht_type, humi, temp), end=" ")
        else:
            print('DHT{0}, humidity & temperature: {1}'.format(
                  dht.dht_type, temp), end=" ")
        print('Visible %03d UV %.2f IR %03d' % (SI1145.ReadVisible,
              SI1145.ReadUV / 100, SI1145.ReadIR), end=" ")
        print(f"Soil humdity: {soil_sensor.read_raw(soil_sensor_pin)}",
              end=' ')
        print('\r', end='')
        time.sleep(0.5)


if __name__ == '__main__':
    main()
