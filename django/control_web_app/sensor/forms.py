from django import forms

from .models import Sensor
from room.models import Room

class Sensor_form(forms.ModelForm):
    LOCATION_CHOICES = [("indoors", "Indoors"), ("outdoors", "Outdoors"),("boiler", "Boiler")]
    
    # [("value saved", "Text seen in select"), ("same", "same")]
    room_choices = [(None, "----")]
    # rooms_set = Room.objects.all()
    # for room in rooms_set:
    #     room_choices.append((room.id, room.room_name))

    location = forms.CharField(label='Choose where sensor is located:', widget=forms.RadioSelect(choices=LOCATION_CHOICES))
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={ "rows": 5 }))
    class Meta:
        model = Sensor
        fields = "__all__"
        