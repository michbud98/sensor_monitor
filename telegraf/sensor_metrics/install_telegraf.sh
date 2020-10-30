DEBUG=0

install_telegraf()
{
	echo "Installing telegraf"
	[ $DEBUG -eq 1 ] && set -x
	apt-get update

	# Add the InfluxData key
	curl -sL https://repos.influxdata.com/influxdb.key | sudo apt-key add -
	echo "deb https://repos.influxdata.com/debian buster stable" | sudo tee /etc/apt/sources.list.d/influxdb.list

	apt-get update && apt-get install telegraf
}

install_configuration()
{
	[ $DEBUG -eq 1 ] && set -x
	echo "Replacing default telegraf service file with modified telegraf service file"
	cp -f telegraf.service /etc/systemd/system/multi-user.target.wants/telegraf.service
	RC=$?
	if [ $RC -ne 0 ]; then
		echo "ERROR: Cannot replace default telegraf service file at /etc/systemd/system/multi-user.target.wants/telegraf.service"
	else
		echo "SUCCESS: Service /etc/systemd/system/multi-user.target.wants/telegraf.service modified"
	fi

	echo "Replacing default config file with sensor data config file"
	cp -f telegraf_sensor_data.conf /etc/telegraf/telegraf.conf
	RC=$?
	if [ $RC -ne 0 ]; then
		echo "ERROR: Cannot replace default config file at /etc/telegraf/telegraf.conf"
	else
		echo "SUCCESS: Config at /etc/telegraf/telegraf.conf replaced"
	fi

	echo "Placing custom python script to telegraf config dir"
	cp ../python_scripts/raspberry_pi_save_weather_stats/get_weather_data.py /etc/telegraf/
	RC=$?	
	if [ $RC -ne 0 ]; then
		echo "ERROR: Cannot place python script in telegraf config directory /etc/telegraf"
	else
		echo "SUCCESS: get_weather_data.py placed in /etc/telegraf/get_weather_data.py"
	fi

	echo "Changing get_weather_data.py ownership to pi"
	chown pi /etc/telegraf/get_weather_data.py && chgrp pi /etc/telegraf/get_weather_data.py
	RC=$?
	
	if [ $RC -ne 0 ]; then
		echo "ERROR: Cannot change ownership of get_weather_data.py to user pi"
	else	
		echo "SUCCESS: ownership of file get_weather_data changed to user pi"
	fi
}

#TODO Add code for setting env variables
# Prints help
usage()
{
	echo "install_telegraf.sh [-dh]"
}

while getopts dh Opt; do
  case "$Opt" in
    d)  DEBUG=1 ;;
    h)  usage
        exit 0 ;;
    \?) usage; exit 1 ;;
  esac
done
shift `expr $OPTIND - 1`

# Install telegraf on sensor
install_telegraf
# Install telegraf configuration and scripts at /etc/telegraf
install_configuration

