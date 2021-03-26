from django.db import models
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os
from adaptor.model import CsvModel
from adaptor.fields import DateField, DecimalField, CharField, IntegerField
from django import forms



class OverwriteStorage(FileSystemStorage):

    def get_available_name(self, name, max_length=None):
        # If the filename already exists, remove it as if it was a true file system
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name

class UploadModel(models.Model):
    files = models.FileField(upload_to="CSVFiles/",  storage=OverwriteStorage())


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
    id = models.AutoField(primary_key=True)
    consumption = models.DecimalField(max_digits=10, decimal_places=5)
    meter_id = models.ForeignKey(Meter, on_delete=models.CASCADE)
    reading_date_time = models.DateTimeField(auto_now=False, default=None)

    def __str__(self):
        return f"{self.meter_id} consumption in {self.reading_date_time}"

