from django.db import models
from adaptor.fields import DateField, DecimalField, CharField, IntegerField
from django import forms



class Hotel(models.Model):
    id   =  models.CharField(max_length=20, primary_key=True)
    name =  models.CharField(max_length=100)
    
    def __str__(self):
        return self.name


class Meter(models.Model):
    building_id  = models.ForeignKey(Hotel, on_delete=models.CASCADE, default=None)
    id   =  models.CharField(max_length=50, primary_key=True)
    fuel =  models.CharField(max_length=50)
    unit =  models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.building_id} Hotel' {self.fuel} Meter "


class Consumption(models.Model):
    consumption = models.DecimalField(max_digits=10, decimal_places=5)
    meter_id = models.ForeignKey(Meter, on_delete=models.CASCADE, primary_key=True)
    reading_date_time = models.DateTimeField(auto_now=False, default=None)

    def __str__(self):
        return f"{self.meter_id} consumption in {self.reading_date_time}"

