#!/usr/bin/env python3

import sys, getopt
import requests
from bs4 import BeautifulSoup
import re

def get_sensor_data_html(sensor_url:str) -> str:
    """
    Gets html from nodemcu sensor
    :param sensor_url: url to sensor
    :return:  String with html
    """
    html = requests.get(sensor_url)
    return html

def get_value_from_sensor(html:str, regex:str) -> int:
    """
    Separates value set by regex using BeautifulSoup
    :param html: html from sensor
    :param regex: Regular expression specifying value we want (recommend finding unit of value)
    :return:  value in integer
    """
    soup = BeautifulSoup(html.content, 'html.parser')
    results = soup.find_all('td', class_="r")
    for result in results:
        x = re.search(regex , result.text.strip()) # example "°[cC]$"
        if x:
            return get_int_value(result.text.strip(), regex)
        else:
            continue

def get_int_value(value_str:str, regex:str) -> int:
    """
    Changes value from string to int
    :param value_str: value in string
    :param regex: Regular expression specifying unit of value we need to remove from string
    :return:  value in integer
    """
    # r.sub finds charakters specified by regex and replaces them with empty string
    value = float(re.sub(regex, "", value_str))
    return value
    
#TODO Add humidity after sensor is upgraded
def main(argumentList):
    http = ""
    options = "ht:"
    long_options = ["help", "http"]

    arguments, values = getopt.getopt(argumentList, options, long_options)

    for currentArgument, currentValue in arguments:
        
        if currentArgument in ("-h", "--Help"):
            print ("get_weather_data_nodemcu.py [-h] -t <http-adress-of-sensor>")
            sys.exit()

        elif currentArgument in ("-t", "--http"):
            http = currentValue
    
    
    sensor_html = get_sensor_data_html(http) # "http://192.168.77.108/values"
    print("sensor_temperature temperature={}".format(get_value_from_sensor(sensor_html, "°[cC]$")))
    print("sensor_humidity humidity={}".format(get_value_from_sensor(sensor_html, "%$")))
    

if __name__ == "__main__":
    main(sys.argv[1:])