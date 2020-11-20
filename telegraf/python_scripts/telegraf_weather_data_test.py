#!/usr/bin/env python3

import sys
import time
import getopt

import random

from subprocess import PIPE, Popen, check_output

import platform  # For getting the operating system name
import subprocess  # For executing a shell command

import traceback

def main(argv):
    try:
        #temperature = bme280.get_temperature()
        temperature = random.randint(-20,40)
        pressure = random.randint(0,1000)
        humidity = random.randint(0,100)
        print("sensor_temperature temperature={}".format(temperature))
        print("sensor_pressure pressure={}".format(pressure))
        print("sensor_humidity humidity={}".format(humidity))
    except:
        print(traceback.format_exc())
        

if __name__ == "__main__":
    main(sys.argv[1:])


