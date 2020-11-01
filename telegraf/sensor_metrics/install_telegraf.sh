DEBUG=0
HOSTNAME=""
INFLUX_HOST=""
INFLUX_TOKEN=""
INFLUX_ORG=""
INFLUX_BUCKET="" 

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
#TODO Add code for saving influx enviromental variables

enter_env_var_values()
{
	echo "Creating file for enviromental variables"
	[ $DEBUG -eq 1 ] && set -x
	# Methods obtaining values of influx env variables from user
	enter_sensor_name
	enter_influx_host
	enter_influx_token
	enter_influx_org
	enter_influx_bucket	

	# Last comfirmation before saving into /etc/default/telegraf
	comfirm_env_var_values
	
}

comfirm_env_var_values()
{
	while true; do
		printf "Variables saved in file /etc/default/telegraf
		Hostname: $HOSTNAME
		Influx host adress: $INFLUX_HOST
		Influx token: $INFLUX_TOKEN
		Influx organization: $INFLUX_ORG
		Influx bucket: $INFLUX_BUCKET \n"
		read -p "Change Sensor (N)ame, (H)ost address, (T)oken, (O)rganization, (B)ucket, (R)esume, (E)nd program: " USER_INPUT
		USER_INPUT=$(echo $USER_INPUT | tr '[:upper:]' '[:lower:]')
		
		case "$USER_INPUT" in
			n) enter_sensor_name ;;
			h) enter_influx_host ;;
			t) enter_influx_token ;;
			o) enter_influx_org ;;
			b) enter_influx_bucket ;;
			r) 
			echo "Saving env variables vill be added later"
			break ;;
			e) 
			echo "Closing program. You can later edit /etc/default/telegraf to add env variables for telegraf config"
			exit 0 ;;
			\?) 
			echo "Wrong argument. Please try again."
			continue ;;
		esac
	done
}

# Setting hostname for sensor
# On empty string uses default value
enter_sensor_name()
{
	while true; do
		read -p "Enter sensor name (Default used on empty string) : " HOSTNAME
		if [ -z "$HOSTNAME" ]; then
			HOSTNAME="Default Value"
			echo "You entered value empty string. Default hostname will be used."
		else
			echo "You entered value $HOSTNAME as sensor name"
		fi
		read -p "Is this correct [y/n]?" USER_INPUT
		USER_INPUT=$(echo $USER_INPUT | tr '[:upper:]' '[:lower:]')
		if [ $USER_INPUT = "y" ]; then
			break
		elif [ $USER_INPUT = "n" ]; then
			continue
		fi

	done
}

# Checks if value is not empty and requests user to comfirm value which he entered
# Return 0 (true) or 1 (false) which is used by other methods
enter_value_check()
{
	arg1=$1
	arg2=$2

	if [ -z "$arg1" ]; then
		echo "ERROR: $2 cant be empty. Type it again."
		return 1
	fi
	echo "You entered value $arg1 as $arg2"
	read -p "Is this correct [y/n]?" USER_INPUT
	USER_INPUT=$(echo $USER_INPUT | tr '[:upper:]' '[:lower:]')
	if [ $USER_INPUT = "y" ]; then
		return 0
	elif [ $USER_INPUT = "n" ]; then
		return 1
	fi
}

enter_influx_host()
{
	while true; do
		read -p "Enter influx host adress: " INFLUX_HOST
		enter_value_check "$INFLUX_HOST" "Influx host adress"
		RC=$?
		[ $RC -eq 0 ] && break
	done
}


enter_influx_token()
{
	while true; do
		read -p "Enter influx token: " INFLUX_TOKEN
		enter_value_check "$INFLUX_TOKEN" "Influx token"
		RC=$?
		[ $RC -eq 0 ] && break
	done
}

enter_influx_org()
{
	while true; do
		read -p "Enter influx organization: " INFLUX_ORG
		enter_value_check "$INFLUX_ORG" "Influx organization"
		RC=$?
		[ $RC -eq 0 ] && break
	done
}

enter_influx_bucket()
{
	while true; do
		read -p "Enter influx bucket name: " INFLUX_BUCKET
		enter_value_check "$INFLUX_BUCKET" "Influx bucket name"
		RC=$?
		[ $RC -eq 0 ] && break
	done
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
# Encapsulates Methods obtaining values of influx env variables from user 
enter_env_var_values

