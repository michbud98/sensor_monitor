from django.shortcuts import render

from basic_values import queries

# Create your views here.
def basic_values_view(request, *args, **kwargs):
    my_context = {
        "temperature_indoors" : queries.last_indoors_temperature,
        "pressure_indoors" : queries.last_indoors_pressure,
        "humidity_indoors" : queries.last_indoors_humidity,
        "temperature_outdoors" : queries.last_outdoors_temperature,
        "pressure_outdoors" : queries.last_outdoors_pressure,
        "humidity_outdoors" : queries.last_outdoors_humidity

    }
    return render(request, "basic_values.html", my_context)