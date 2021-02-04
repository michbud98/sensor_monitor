from django.shortcuts import render
from django.shortcuts import redirect

from sensor_control.models import Sensor
from .models import Room

# Create your views here.
def room_list_view(request):
    rooms_set = Room.objects.all()
    my_context = {
        "rooms_set": rooms_set
    }
    return render(request, "room_list.html", my_context)

# def room_create_view(request):
#     if request.method == "POST":
#         form = Room_form(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect(room_list_view)
#     else:
#         form = Room_form()
#         my_context ={
#             'form':form,
#         }
#     return render(request, "sensor_create.html", my_context)