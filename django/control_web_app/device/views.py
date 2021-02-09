from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect

from .models import Device, Thermo_head, Sunblind
from .forms import Device_form, Thermo_head_form, Sunblind_form, Thermo_head_values_form, Sunblind_values_form

# Create your views here.
def device_list_view(request):
    devices_set = Device.objects.all()
    my_context = {
        "devices_set": devices_set
    }
    return render(request, "device_list.html", my_context)

def device_create_view(request):
    if request.method == "POST":
        device_form = Device_form(request.POST)
        if device_form.is_valid():
            # REWORK Use device_types from model Devices
            if device_form.cleaned_data.get("device_type") == "thermo_head":
                form = Thermo_head_form(request.POST)
            elif device_form.cleaned_data.get("device_type") == "sunblind":
                form = Sunblind_form(request.POST)
            form.save()
            return redirect(device_list_view)
    else:
        form = Device_form()
        my_context ={
            'form':form,
        }
    return render(request, "device_create.html", my_context)

def device_update_view(request, device_id):
    form = None
    obj = get_object_or_404(Device, device_id=device_id)
    form = Device_form(request.POST or None, instance=obj)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect(device_list_view)
    my_context = {
        'form': form
    }
    return render(request, "device_create.html", my_context)

def device_detail_view(request, device_id):
    device = get_object_or_404(Device, device_id=device_id)
    thermo_head = None
    sunblind = None
    # REWORK Use device_types from model Devices
    if device.device_type == "thermo_head":
        thermo_head = get_object_or_404(Thermo_head, device_id=device_id)
    elif device.device_type == "sunblind":
        sunblind = get_object_or_404(Sunblind, device_id=device_id)
    my_context = {
        "device": device,
        "thermo_head": thermo_head,
        "sunblind": sunblind,
    }
    return render(request, "device_detail.html", my_context)
    

def device_values_edit_view(request, device_id, room_id):
    device = get_object_or_404(Device, device_id=device_id)
    thermo_head = None
    sunblind = None
    # REWORK Use device_types from model Devices
    if device.device_type == "thermo_head":
        thermo_head = get_object_or_404(Thermo_head, device_id=device_id)
        initial_data = { "set_heat_value": thermo_head.set_heat_value }
        form = Thermo_head_values_form(request.POST or None, initial=initial_data, instance=thermo_head)

    elif device.device_type == "sunblind":
        sunblind = get_object_or_404(Sunblind, device_id=device_id)
        initial_data = { "set_open_value": sunblind.set_open_value }
        form = Sunblind_values_form(request.POST or None, initial=initial_data, instance=sunblind)
    
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect(device_detail_view, device_id=device_id)
    my_context = {
        'form': form,
        "device": device,
        "thermo_head": thermo_head,
        "sunblind": sunblind,
        "room_id": room_id
    }
    return render(request, "device_values_edit.html", my_context)

def device_remove_view(request, device_id):
    obj = get_object_or_404(Device, device_id=device_id)
    if request.method == "POST":
        obj.delete()
        return redirect(device_list_view)
    my_context = {
        "obj": obj
    }
    return render(request, "device_delete.html", my_context)