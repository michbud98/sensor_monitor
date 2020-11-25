#!/usr/bin/env python3

import sys
import time
import getopt

from bme280 import BME280

try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus

from subprocess import PIPE, Popen, check_output

import platform  # For getting the operating system name
import subprocess  # For executing a shell command

import traceback


bus = SMBus(1)
bme280 = BME280(i2c_dev=bus)


def main(argv):
    try:
        # TODO find out which temperature collection is more accurate raw/compensated
        temperature = bme280.get_temperature()
        pressure = bme280.get_pressure()
        humidity = bme280.get_humidity()
        print("sensor_temperature temperature={}".format(temperature))
        print("sensor_pressure pressure={}".format(pressure))
        print("sensor_humidity humidity={}".format(humidity))
    except:
        print(traceback.format_exc())
        

if __name__ == "__main__":
    main(sys.argv[1:])


