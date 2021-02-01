from django import forms

from .models import Sensor

class Sensor_form(forms.ModelForm):
    LOCATION_CHOICES = [("indoors", "Indoors"), ("outdoors", "Outdoors")]
    location = forms.CharField(label='Choose where sensor is located:', widget=forms.RadioSelect(choices=LOCATION_CHOICES))
    class Meta:
        model = Sensor
        fields = "__all__"
        labels = {
            "room" : 'Choose room (if its outdoors leave blank):'
        }