from django.shortcuts import render

from room_control import queries


# Create your views here.
def sensor_list_view(request, *args, **kwargs):
    unset_list, set_list = queries.sort_sensor_ids(queries.query_all_tags())
    my_context = {
        "sensor_id_list_nonset": unset_list,
        "sensor_id_list_set": set_list,
    }
    return render(request, "sensor_list.html", my_context)
