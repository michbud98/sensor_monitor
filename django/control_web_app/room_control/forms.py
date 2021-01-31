from django import forms

from .models import Sensor

class Sensor_form(forms.ModelForm):
    class Meta:
        model = Sensor
        fields = [
            "sensor_id",
            "hostname",
            "location",
            "room",
            "description"
        ]