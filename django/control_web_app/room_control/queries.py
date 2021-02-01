from myutils.get_influx_data import query_field_val_from_db, \
    query_val_from_db, query_all_tag_values, get_bucket

from .models import Sensor

from typing import Dict, List, Tuple


def sort_sensor_ids(sensor_id_list: List[str]) -> Tuple[List[str], List[Sensor]]:
    """
    Sorts sensor ids between two lists based on their availability in the django connected database. 
    If sensor is in the database it has set location.

    :param sensor_id_list: List of sensor_ids collected from Influxdb
    :return: Tuple with list of sensor ids without set location and list of class Sensor that contains sensor with set location (in database)
    """
    sensor_id_nonset = []
    sensor_id_set = []
    for sensor_id in sensor_id_list:
        if Sensor.objects.filter(sensor_id=sensor_id).count() == 1:
            sensor_id_set.append(Sensor.objects.get(sensor_id=sensor_id))
        else:
            sensor_id_nonset.append(sensor_id)

    return sensor_id_nonset, sensor_id_set


def create_hostname_dict(sensor_id_list: List[str]) -> Dict[str, str]:
    """
    :param sensor_id_list: List of sensor_ids collected from Influxdb
    :return: Dictionary with sensor ids as keys and hostnames as values
    """
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
    |> distinct()".format(get_bucket(), sensor_id)
    return query_val_from_db(hostname_query)[0]
