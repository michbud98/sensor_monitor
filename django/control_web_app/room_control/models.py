from django.db import models

# Create your models here.
class Sensor(models.Model):
    sensor_id = models.CharField(max_length=30, unique=True)
    hostname = models.CharField(max_length=30, null=True)
    location = models.CharField(max_length=30, default="nonset")
    room = models.CharField(max_length=30, default="nonset")
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.sensor_id