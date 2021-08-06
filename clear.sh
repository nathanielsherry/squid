#!/bin/bash
cd "$(dirname "$0")"

#RPi light controls
echo 1 >/sys/class/leds/led0/brightness
echo 1 >/sys/class/leds/led1/brightness

squid example-clear.yaml
