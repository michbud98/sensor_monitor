from django.shortcuts import render

from room_control import queries

# Create your views here.
def sensor_list_view(request, *args, **kwargs):
    my_context = {
        "sensor_id_list" : queries.query_all_tags,
    }
    return render(request, "sensor_list.html", my_context)

    