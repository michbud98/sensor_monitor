from django.shortcuts import render

from get_influx_data import query_data_from_influxdb


# Create your views here.

#Shows info about product using id
def show_basic_temp_values(request):
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

    context = {
        "indoor_result": query_data_from_influxdb(indoors_query)[0][1],
        "outdoor_result": query_data_from_influxdb(outdoors_query)[0][1]
    }
    return render(request, "basic_values.html", context)

