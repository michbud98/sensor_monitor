DEBUG=0

# Installs telegraf on raspberry pi 
install_telegraf()
{
	echo "Installing telegraf"
	[ $DEBUG -eq 1 ] && set -x
	apt-get update

	# Add the InfluxData key
	curl -sL https://repos.influxdata.com/influxdb.key |  apt-key add -
	echo "deb https://repos.influxdata.com/debian buster stable" |  tee /etc/apt/sources.list.d/influxdb.list

	apt-get update && apt-get install -y telegraf 
}

# Installs configuration files and replaces default telegraf service on raspberry pi 
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
	cp -f telegraf_sensor_data_test.conf /etc/telegraf/telegraf.conf
	RC=$?
	if [ $RC -ne 0 ]; then
		echo "ERROR: Cannot replace default config file at /etc/telegraf/telegraf.conf"
	else
		echo "SUCCESS: Config at /etc/telegraf/telegraf.conf replaced"
	fi

	echo "Placing custom python script to telegraf config dir"
	cp python_scripts/telegraf_weather_data_test.py /etc/telegraf/get_weather_data.py
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
		echo "SUCCESS: Ownership of file get_weather_data changed to user pi"
	fi
	
	echo "Creating log file at /var/log/telegraf"
	touch /var/log/telegraf/telegraf.log
	RC=$?

	if [ $RC -ne 0 ]; then
		echo "ERROR: Cannot create log file at /var/log/telegraf"
	else	
		echo "SUCCESS: Log file created at /var/log/telegraf"
	fi

	echo "Changing default logging directory /var/log/telegraf ownership to pi"
	chown -R pi /var/log/telegraf && chgrp -R pi /var/log/telegraf
	RC=$?

	if [ $RC -ne 0 ]; then
		echo "ERROR: Cannot change ownership of logging directory /var/log/telegraf to user pi"
	else	
		echo "SUCCESS: Ownership of logging directory /var/log/telegraf  changed to user pi"
	fi

}

# Saves env variables to /etc/default/telegraf
save_env_var_values()
{
	[ $DEBUG -eq 1 ] && set -x
	set -e
	echo "Overwriting default telegraf env variables file at /etc/default/telegraf with your env variables"
	echo "HOSTNAME=\"$HOSTNAME\"" |  tee /etc/default/telegraf > /dev/null
	RC=$?
	if [ $RC -ne 0 ]; then
		echo "ERROR: Cannot write HOSTNAME to /etc/default/telegraf"
	else	
		echo "SUCCESS: HOSTNAME written to /etc/default/telegraf"
	fi

	echo "INFLUX_HOST=\"$INFLUX_HOST\"" |  tee -a /etc/default/telegraf > /dev/null
	RC=$?
	if [ $RC -ne 0 ]; then
		echo "ERROR: Cannot write INFLUX_HOST to /etc/default/telegraf"
	else	
		echo "SUCCESS: INFLUX_HOST written to /etc/default/telegraf"
	fi

	echo "INFLUX_TOKEN=\"$INFLUX_TOKEN\"" |  tee -a /etc/default/telegraf > /dev/null
	RC=$?
	if [ $RC -ne 0 ]; then
		echo "ERROR: Cannot write INFLUX_TOKEN to /etc/default/telegraf"
	else	
		echo "SUCCESS: INFLUX_TOKEN written to /etc/default/telegraf"
	fi

	echo "INFLUX_ORG=\"$INFLUX_ORG\"" |  tee -a /etc/default/telegraf > /dev/null
	RC=$?
	if [ $RC -ne 0 ]; then
		echo "ERROR: Cannot write INFLUX_ORG to /etc/default/telegraf"
	else	
		echo "SUCCESS: INFLUX_ORG written to /etc/default/telegraf"
	fi

	echo "INFLUX_BUCKET=\"$INFLUX_BUCKET\"" |  tee -a /etc/default/telegraf > /dev/null
	RC=$?
	if [ $RC -ne 0 ]; then
		echo "ERROR: Cannot write INFLUX_BUCKET to /etc/default/telegraf"
	else	
		echo "SUCCESS: INFLUX_BUCKET written to /etc/default/telegraf"
	fi
	
	echo "Installation successfull"
	echo "RECOMMENDATION: Reboot sensor for telegraf config to take effect"
}

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
# Saves to env variables to /etc/default/telegraf file
save_env_var_values


