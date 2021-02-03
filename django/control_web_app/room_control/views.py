from django.shortcuts import render

from sensor_control.models import Sensor

# Create your views here.
def room_list_view(request):

    indoors_sensors_set = Sensor.objects.filter(location="indoors")
    my_context = {
        "indoors_sensors_set": indoors_sensors_set
    }
    return render(request, "room_list.html", my_context)