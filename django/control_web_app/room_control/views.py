from django.shortcuts import render
from django.template.defaulttags import register
from django.shortcuts import redirect

from room_control import queries
from .models import Sensor
from .forms import Sensor_form


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

# Create your views here.
def sensor_list_view(request):
    hostname_dict = queries.add_hostname_to_sensor_ids(queries.query_all_tag_values("sensor_id"))
    unset_list, set_list = queries.sort_sensor_ids(queries.query_all_tag_values("sensor_id"))
    my_context = {
        "hostname_dict" : hostname_dict,
        "sensor_id_list_nonset": unset_list,
        "sensor_id_list_set": set_list,
    }
    return render(request, "sensor_list.html", my_context)

def sensor_create_view(request, sensor_id, hostname):
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


