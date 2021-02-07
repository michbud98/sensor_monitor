from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect

from .models import Device
from .forms import Device_form


# Create your views here.
def device_list_view(request):
    devices_set = Device.objects.all()
    print(devices_set)
    my_context = {
        "devices_set": devices_set
    }
    return render(request, "device_list.html", my_context)

def device_create_view(request):
    if request.method == "POST":
        form = Device_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect(device_list_view)
    else:
        form = Device_form()
        my_context ={
            'form':form,
        }
    return render(request, "room_create.html", my_context)

def device_update_view(request, device_id):
    obj = get_object_or_404(Device, device_id=device_id)
    form = Device_form(request.POST or None, instance=obj)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect(device_list_view)
    if form.is_valid():
        form.save()
    context = {
        'form': form
    }
    return render(request, "device_create.html", context)

def device_detail_view(request, device_id):
    obj = get_object_or_404(Device, device_id=device_id)
    
    my_context = {
            "obj" : obj,
        }
    return render(request, "device_detail.html", my_context)

def device_remove_view(request, device_id):
    obj = get_object_or_404(Device, device_id=device_id)
    if request.method == "POST":
        obj.delete()
        return redirect(device_list_view)
    my_context = {
        "obj": obj
    }
    return render(request, "device_delete.html", my_context)