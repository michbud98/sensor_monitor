from django import forms

from .models import Sensor
from room_control.models import Room

class Sensor_form(forms.ModelForm):
    LOCATION_CHOICES = [("indoors", "Indoors"), ("outdoors", "Outdoors")]
    
    # [("value saved", "Text seen in select"), ("same", "same")]
    room_choices = [(None, "----")]
    # rooms_set = Room.objects.all()
    # for room in rooms_set:
    #     room_choices.append((room.id, room.room_name))

    location = forms.CharField(label='Choose where sensor is located:', widget=forms.RadioSelect(choices=LOCATION_CHOICES))
    class Meta:
        model = Sensor
        fields = "__all__"