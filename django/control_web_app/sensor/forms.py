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
        
    def clean_room(self):
        location = self.cleaned_data.get("location")
        room = self.cleaned_data.get("room")
        print(location)
        print(room)

        if location == "outdoors" and room is not None:
            raise forms.ValidationError("Location outdoors can't have set room")
        if location == "boiler" and room is not None:
            raise forms.ValidationError("Boiler can't have set room")
        else:
            return room
        
