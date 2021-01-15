from django.shortcuts import render

import querries


# Create your views here.

#Shows info about product using id
def show_basic_values(request):
    context = {
        "temp_indoor": querries.last_indoors_temperature(),
        "pressure_indoor":querries.last_indoors_pressure(),
        "humidity_indoors":querries.last_indoors_humidity(),
        "light_indoors":querries.last_indoors_light(),
        "temp_outdoor": querries.last_outdoors_temperature(),
        "pressure_outdoors": querries.last_outdoors_pressure(),
        "humidity_outdoors": querries.last_outdoors_humidity()
         
    }
    return render(request, "basic_values.html", context)

