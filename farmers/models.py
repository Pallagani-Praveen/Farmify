from django.db import models

# Create your models here.

class PinToLatLong(models.Model):
    pin = models.IntegerField()
    lat = models.FloatField()
    long = models.FloatField()

    def __str__(self):
        return str(self.pin)
