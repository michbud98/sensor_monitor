from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.template.defaulttags import register

from sensor_control.models import Sensor

from .models import Room
from .forms import Room_form
from . import queries


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

# Create your views here.
def room_list_view(request):
    rooms_set = Room.objects.all()
    my_context = {
        "rooms_set": rooms_set
    }
    return render(request, "room_list.html", my_context)

def room_create_view(request):
    if request.method == "POST":
        form = Room_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect(room_list_view)
    else:
        form = Room_form()
        my_context ={
            'form':form,
        }
    return render(request, "room_create.html", my_context)

def room_update_view(request, room_id):
    obj = get_object_or_404(Room, id=room_id)
    form = Room_form(request.POST or None, instance=obj)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect(room_list_view)
    if form.is_valid():
        form.save()
    context = {
        'form': form
    }
    return render(request, "room_create.html", context)

def room_detail_view(request, room_id):
    sensors_set = Sensor.objects.filter(room=room_id)
    obj = get_object_or_404(Room, id=room_id)
    temp_dict = queries.create_temp_dict(sensors_set)
    pressure_dict = queries.create_pressure_dict(sensors_set)
    humidity_dict = queries.create_humidity_dict(sensors_set)
    my_context = {
            "obj" : obj,
            "sensors_set": sensors_set,
            "temp_dict": temp_dict,
            "pressure_dict": pressure_dict,
            "humidity_dict": humidity_dict,
        }
    return render(request, "room_detail.html", my_context)

def room_remove_view(request, room_id):
    obj = get_object_or_404(Room, id=room_id)
    if request.method == "POST":
        obj.delete()
        return redirect(room_list_view)
    my_context = {
        "obj": obj
    }
    return render(request, "room_delete.html", my_context)