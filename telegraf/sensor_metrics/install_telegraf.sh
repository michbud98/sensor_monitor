#TODO Create methods and method calls
apt-get update

# Add the InfluxData key
curl -sL https://repos.influxdata.com/influxdb.key | sudo apt-key add -
echo "deb https://repos.influxdata.com/debian buster stable" | sudo tee /etc/apt/sources.list.d/influxdb.list

apt-get update && apt-get install telegraf

#TODO Replace these blocks with propper debug messages
echo "Replacing default telegraf service file with modified telegraf service file"
cp -f telegraf.service /etc/systemd/system/multi-user.target.wants/telegraf.service
echo "SUCCESS: Service /etc/systemd/system/multi-user.target.wants/telegraf.service modified"

echo "Replacing default config file with sensor data config file"
cp -f telegraf_sensor_data.conf /etc/telegraf/telegraf.conf
echo "SUCCESS: Config at /etc/telegraf/telegraf.conf replaced"

echo "Placing custom python script to telegraf config dir"
cp ../python_scripts/raspberry_pi_save_weather_stats/get_weather_data.py /etc/telegraf/
echo "SUCCESS: get_weather_data.py placed in /etc/telegraf/get_weather_data.py"

echo "Changing get_weather_data.py ownership to pi"
chown pi /etc/telegraf/get_weather_data.py && chgrp pi /etc/telegraf/get_weather_data.py
echo "SUCCESS: ownership of file get_weather_data changed to user pi"

#TODO Add code for setting env variables
