docker run --rm -it --network=sensor_monitor_default --name influxdb_client \
--link=influxdb_database influxdb:1.8.3 influx -host influxdb_database 
