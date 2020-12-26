docker run --rm -d --name influxdb2 \
-v $PWD/database_files:/var/lib/influxdb \
-p 9999:9999 \
voidborn/rpi_influxdb2
