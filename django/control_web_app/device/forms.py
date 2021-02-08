from django import forms

from .models import Device, Thermo_head, Sunblind

class Device_form(forms.ModelForm):
    class Meta:
        model = Device
        fields = [
            "device_id",
            "device_type",
            "room"
        ]

class Thermo_head_form(Device_form):
    class Meta(Device_form.Meta):
        model = Thermo_head

class Sunblind_form(Device_form):
    class Meta(Device_form.Meta):
        model = Sunblind
        
class Thermo_head_values_form(Device_form):
    class Meta(Device_form.Meta):
        model = Thermo_head
        fields = [
            "set_heat_value",
        ]
        labels = {
            'set_heat_value': "Heat value"
        }

class Sunblind_values_form(Device_form):
    class Meta(Device_form.Meta):
        model = Sunblind
        fields = [
            "set_open_value",
        ]