#!/bin/bash
scp -r ./src/* pi@raspberrypi.local:/home/pi/comp0016-farmbeats/src
scp -r install.sh pi@raspberrypi.local:/home/pi/comp0016-farmbeats/
scp -r services/* pi@raspberrypi.local:/home/pi/comp0016-farmbeats/services

