from django.db import models

# Create your models here.
class Sensor(models.Model):
    sensor_id = models.CharField(max_length=30)
    location = models.CharField(max_length=30)
    room = models.CharField(max_length=30,blank=True, null=True)
    description = models.TextField(blank=True, null=True)