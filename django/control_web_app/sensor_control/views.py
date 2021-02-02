from django.shortcuts import render, get_object_or_404
from django.template.defaulttags import register
from django.shortcuts import redirect

from sensor_control import queries
from .models import Sensor
from .forms import Sensor_form


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

# Create your views here.
def sensor_list_view(request):
    hostname_dict = queries.create_hostname_dict(queries.query_all_tag_values("sensor_id"))
    unset_list, set_list = queries.sort_sensor_ids(queries.query_all_tag_values("sensor_id"))
    my_context = {
        "hostname_dict" : hostname_dict,
        "sensor_id_list_nonset": unset_list,
        "sensor_id_list_set": set_list,
    }
    return render(request, "sensor_list.html", my_context)

def sensor_create_view(request, sensor_id, hostname):
    # TODO Might be a good idea to add some try catch or something like that
    initial_data = { "sensor_id": sensor_id, "hostname": hostname}
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
    if request.method == "POST":
        obj.delete()
        return redirect(sensor_list_view)
    my_context = {
        "obj": obj
    }
    return render(request, "sensor_delete.html", my_context)

def sensor_detail_view(request, sensor_id):
    obj = None
    try:
        obj = Sensor.objects.get(sensor_id=sensor_id)
        temperature = queries.querry_last_sensor_temp(obj.sensor_id)
        pressure = queries.querry_last_sensor_pressure(obj.sensor_id)
        humitidy = queries.querry_last_sensor_humidity(obj.sensor_id)
    except Sensor.DoesNotExist:
        temperature = queries.querry_last_sensor_temp(sensor_id)
        pressure = queries.querry_last_sensor_pressure(sensor_id)
        humitidy = queries.querry_last_sensor_humidity(sensor_id)

    my_context = {
            "sensor_id": sensor_id,
            "obj" : obj,
            "temperature": temperature,
            "pressure": pressure,
            "humidity": humitidy
        }
    
    return render(request, "sensor_detail.html", my_context)