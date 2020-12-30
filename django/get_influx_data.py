import influxdb_client

bucket = "Sensor_data"
org = "swiftblade1982@gmail.com"
token = "IqVLx0CNb_rm4yh1nebq8x70acTQ0XXMKegq5y98c-d9CK7mc5gyh1qrKrwOQHs52TKD2Nt3D3-GdeZl7ZtKaQ=="
# Store the URL of your InfluxDB instance
url="https://eu-central-1-1.aws.cloud2.influxdata.com"

client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

query_api = client.query_api()

indoors_query = 'from(bucket: "Sensor_data")\
  |> range(start: -1h)\
  |> filter(fn: (r) => r["_measurement"] == "sensor_temperature")\
  |> filter(fn: (r) => r["_field"] == "temperature")\
  |> filter(fn: (r) => r["host"] == "raspberrypi")\
  |> last()'

outdoors_query= 'from(bucket: "Sensor_data")\
  |> range(start: -1h)\
  |> filter(fn: (r) => r["_measurement"] == "sensor_temperature")\
  |> filter(fn: (r) => r["_field"] == "temperature")\
  |> filter(fn: (r) => r["host"] == "telegraf-docker")\
  |> last()'

indoors_result = client.query_api().query(org=org, query=indoors_query)

indoors_result_tuple = []
for table in indoors_result:
    for record in table.records:
        indoors_result_tuple.append((record.get_field(), record.get_value()))

outdoors_result = client.query_api().query(org=org, query=outdoors_query)

outdoors_result_tuple = []
for table in outdoors_result:
    for record in table.records:
        outdoors_result_tuple.append((record.get_field(), record.get_value()))
        
print("Indoors result: {}".format(indoors_result_tuple))
print("Outdoors result: {}".format(outdoors_result_tuple))