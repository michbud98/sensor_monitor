from django.shortcuts import render, get_object_or_404
from django.template.defaulttags import register
from django.shortcuts import redirect

from sensor_control import queries
from .models import Sensor
from .forms import Sensor_form
from room_control.models import Room


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

# Create your views here.
def sensor_list_view(request):
    unset_list, set_list = queries.sort_sensor_ids(queries.query_all_tag_values("sensor_id"))
    hostname_dict = queries.create_hostname_dict(queries.query_all_tag_values("sensor_id"))
    sensor_type_dict = queries.create_sensor_type_dict(queries.query_all_tag_values("sensor_id"))
    room_dict = queries.create_room_dict(set_list)
    
    my_context = {
        "hostname_dict" : hostname_dict,
        "sensor_type_dict" : sensor_type_dict,
        "room_dict": room_dict,
        "sensor_id_list_nonset": unset_list,
        "sensor_id_list_set": set_list,
    }
    return render(request, "sensor_list.html", my_context)

def sensor_create_view(request, sensor_id, hostname, sensor_type):
    # TODO Might be a good idea to add some try catch or something like that
    initial_data = { "sensor_id": sensor_id, "hostname": hostname, "sensor_type": sensor_type}
    if request.method == "POST":
        form = Sensor_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect(sensor_list_view)
    else:
        form = Sensor_form(initial=initial_data)
        my_context ={
            'form':form,
        }
    return render(request, "sensor_create.html", my_context)

def sensor_update_view(request, sensor_id):
    obj = get_object_or_404(Sensor, sensor_id=sensor_id)
    form = Sensor_form(request.POST or None, instance=obj)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect(sensor_list_view)
    if form.is_valid():
        form.save()
    context = {
        'form': form
    }
    return render(request, "sensor_create.html", context)

def sensor_remove_view(request, sensor_id):
    obj = get_object_or_404(Sensor, sensor_id=sensor_id)
    room_name = None
    if request.method == "POST":
        obj.delete()
        return redirect(sensor_list_view)
    else:
        if obj.room:
            room_name = get_object_or_404(Room, id=int(obj.room)).__str__()

    my_context = {
        "obj": obj,
        "room_name": room_name
    }
    return render(request, "sensor_delete.html", my_context)

def sensor_detail_view(request, sensor_id):
    obj = None
    room_name = None
    try:
        obj = Sensor.objects.get(sensor_id=sensor_id)
        temperature = queries.query_last_sensor_temp(obj.sensor_id)
        pressure = queries.query_last_sensor_pressure(obj.sensor_id)
        humitidy = queries.query_last_sensor_humidity(obj.sensor_id)
        if obj.room:
            room_name = get_object_or_404(Room, id=int(obj.room)).__str__()
    except Sensor.DoesNotExist:
        temperature = queries.query_last_sensor_temp(sensor_id)
        pressure = queries.query_last_sensor_pressure(sensor_id)
        humitidy = queries.query_last_sensor_humidity(sensor_id)

    my_context = {
            "sensor_id": sensor_id,
            "obj" : obj,
            "room_name": room_name,
            "temperature": temperature,
            "pressure": pressure,
            "humidity": humitidy
        }
    
    return render(request, "sensor_detail.html", my_context)