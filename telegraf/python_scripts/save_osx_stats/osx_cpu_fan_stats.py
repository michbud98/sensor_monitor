#!/usr/bin/env python3

import sys, getopt
import subprocess

def subprocess_cmd(command):
    process = subprocess.Popen(command,stdout=subprocess.PIPE, shell=True)
    stdout, stderr = process.communicate()
    return stdout, stderr

cpu_temp,_ = subprocess_cmd('/usr/local/bin/smc -k TC0P -r | tr -s " " | tr " " "," | cut -d, -f 4')
fan_side,_ = subprocess_cmd('/usr/local/bin/smc -f | grep "Fan ID" | tr -s " " | tr " " "," | cut -d, -f 5')
fan_rpm,_ = subprocess_cmd('/usr/local/bin/smc -f | grep "Actual speed" | tr -s " " | tr " " "," | cut -d, -f 5')
fan_percent= (int(fan_rpm) - 1290) * 100 / 4900

print("cpu_temp temp={}".format(float(cpu_temp)))
print("fan_speed,side={} rpm={},percent={}".format(fan_side.decode("utf-8").strip(),int(fan_rpm),fan_percent))