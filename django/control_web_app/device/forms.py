from django import forms

from .models import Device

class Device_form(forms.ModelForm):
    class Meta:
        model = Device
        fields = "__all__"
        