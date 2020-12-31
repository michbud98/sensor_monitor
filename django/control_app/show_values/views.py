from django.shortcuts import render

from get_influx_data import query_data_from_influxdb


# Create your views here.

#Shows info about product using id
def show_basic_temp_values(request):
    temp_indoors_query = 'from(bucket: "Sensor_data")\
    |> range(start: -1h)\
    |> filter(fn: (r) => r["_measurement"] == "sensor_temperature")\
    |> filter(fn: (r) => r["_field"] == "temperature")\
    |> filter(fn: (r) => r["host"] == "raspberrypi")\
    |> last()'

    temp_outdoors_query= 'from(bucket: "Sensor_data")\
    |> range(start: -1h)\
    |> filter(fn: (r) => r["_measurement"] == "sensor_temperature")\
    |> filter(fn: (r) => r["_field"] == "temperature")\
    |> filter(fn: (r) => r["host"] == "telegraf-docker")\
    |> last()'

    light_indoors_query= 'from(bucket: "Sensor_data")\
    |> range(start: -1h)\
    |> filter(fn: (r) => r["_measurement"] == "sensor_light")\
    |> filter(fn: (r) => r["_field"] == "light")\
    |> filter(fn: (r) => r["host"] == "raspberrypi")\
    |> last()'


    context = {
        "temp_indoor_result": query_data_from_influxdb(temp_indoors_query)[0][1],
        "temp_outdoor_result": query_data_from_influxdb(temp_outdoors_query)[0][1],
        "light_indoors_result": query_data_from_influxdb(light_indoors_query)[0][1]
    }
    return render(request, "basic_values.html", context)

