from django.shortcuts import render

# Create your views here.
def sensor_list_view(request, *args, **kwargs):
    return render(request, "sensor_list.html", {})