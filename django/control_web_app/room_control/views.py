from django.shortcuts import render
from django.template.defaulttags import register

from room_control import queries


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

# Create your views here.
def sensor_list_view(request, *args, **kwargs):
    hostname_dict = queries.add_hostname_to_sensor_ids(queries.query_all_tag_values("sensor_id"))
    unset_list, set_list = queries.sort_sensor_ids(queries.query_all_tag_values("sensor_id"))
    my_context = {
        "hostname_dict" : hostname_dict,
        "sensor_id_list_nonset": unset_list,
        "sensor_id_list_set": set_list,
    }
    return render(request, "sensor_list.html", my_context)
