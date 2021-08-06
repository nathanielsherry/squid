#!/bin/bash
cd "$(dirname "$0")"

#RPi light controls
#turn off the system-board led lights
echo 0 >/sys/class/leds/led0/brightness
echo 0 >/sys/class/leds/led1/brightness

#force-update the time 
ntpdate -s -u time.nist.gov

squid example.yaml
