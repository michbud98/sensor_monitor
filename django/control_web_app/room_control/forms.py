from django import forms

from .models import Sensor

class Sensor_form(forms.ModelForm):
    class Meta:
        model = Sensor
        fields = '__all__' # uses all fields of model