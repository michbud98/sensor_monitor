import os
from pathlib import Path

import influxdb_client
from typing import Dict, List, Tuple

BASE_DIR = Path(__file__).resolve().parent.parent

bucket = "Sensor_data"
org = "swiftblade1982@gmail.com"
# Gets Influx token from file
with open(os.path.join(BASE_DIR, "secrets/influx_cloud_token.txt")) as f:
    token = f.read().strip()
# Store the URL of your InfluxDB instance
url = "https://eu-central-1-1.aws.cloud2.influxdata.com"

client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

query_api = client.query_api()


def query_field_val_from_db(query: str) -> List[tuple]:
    """
    Queries Measurement field and value from InfluxDB database
    :param query: Query which specifies data we want to get from InfluxDB (uses Flux)
    :return: List of tuples (Measurement field name, Measurement value)
    """
    result = client.query_api().query(org=org, query=query)
    results = []
    for table in result:
        for record in table.records:
            results.append((record.get_field(), record.get_value()))
    return results


def query_val_from_db(query: str) -> List[tuple]:
    """
    Queries Measurement value from InfluxDB database
    :param query: Query which specifies data we want to get from InfluxDB (uses Flux)
    :return: List of tuples (Measurement value)
    """
    result = client.query_api().query(org=org, query=query)
    results = []
    for table in result:
        for record in table.records:
            results.append(record.get_value())
    return results


def main():
    query = 'from(bucket: "Sensor_data")\
    |> range(start: -1h)\
    |> filter(fn: (r) => r["_measurement"] == "sensor_temperature")\
    |> filter(fn: (r) => r["_field"] == "temperature")\
    |> filter(fn: (r) => r["host"] == "rpizero2")'
    tag_query = 'import "influxdata/influxdb/v1"\
    v1.tagValues(\
      bucket: "Sensor_data",\
      tag: "sensor_id",\
      predicate: (r) => true,\
      start: -1y)'
    print(query_field_val_from_db(query))
    print(query_val_from_db(tag_query))


if __name__ == "__main__":
    main()
