from myutils.get_influx_data import query_field_val_from_db, query_val_from_db

from .models import Sensor

from typing import Dict, List, Tuple


def sort_sensor_ids(sensor_id_list: List[str]) -> Tuple[List[str], List[Sensor]]:
    """
    :param sensor_id_list: List of sensor_ids collected from Influxdb
    :return: Tuple with list os sensor_ids with set room and list of sensor ids without set room
    """
    sensor_id_nonset = []
    sensor_id_set = []
    for sensor_id in sensor_id_list:
        if Sensor.objects.filter(sensor_id=sensor_id).count() == 1:
            sensor_id_set.append(Sensor.objects.get(sensor_id=sensor_id))
        else:
            sensor_id_nonset.append(sensor_id)

    return sensor_id_nonset, sensor_id_set


def query_all_tags():
    tag_query = 'import "influxdata/influxdb/v1"\
    v1.tagValues(\
      bucket: "Sensor_data",\
      tag: "sensor_id",\
      predicate: (r) => true,\
      start: -1y)'
    return query_val_from_db(tag_query)


def add_hostname_to_sensor_ids(sensor_id_list: List[str]):
    sensor_id_hostnames: Dict[str] = {}
    for sensor_id in sensor_id_list:
        sensor_id_hostnames[sensor_id] = query_sensor_hostname(sensor_id)
    return sensor_id_hostnames

def query_sensor_hostname(sensor_id: str):
    hostname_query = "from(bucket: \"{}\")\
    |> range(start: -30d)\
    |> filter(fn: (r) => r.sensor_id == \"{}\")\
    |> keyValues(keyColumns: [\"host\"])\
    |> keep(columns: [\"_value\"])\
    |> group()\
    |> distinct()".format("Sensor_data", sensor_id)
    return query_val_from_db(hostname_query)[0]
