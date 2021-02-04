from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect

from sensor_control.models import Sensor
from .models import Room
from .forms import Room_form

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
    obj = get_object_or_404(Room, id=room_id)
    my_context = {
            "obj" : obj,
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