docker run -d --rm --name telegraf \
-v $PWD/telegraf.conf:/etc/telegraf/telegraf.conf:ro \
--link influxdb_database \
telegraf