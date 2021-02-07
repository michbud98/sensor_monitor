from django.db import models
from django.urls import reverse
from room.models import Room

# Create your models here.
class Device(models.Model):
    DEVICE_TYPES = (
        ('sunblind', 'sunblind'),
        ('thermostatic head', 'thermostatic head'),
    )
    device_id = models.CharField(max_length=30, unique=True)
    device_type = models.CharField(max_length=30, choices=DEVICE_TYPES)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.device_id