from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import UploadFileForm
from .models import UploadModel
from django.views.generic import CreateView, DetailView, ListView
from .models import Meter, Hotel, Consumption, UploadModel
from django.conf import settings
import os, csv
from django.shortcuts import render
from django.http import HttpResponse
from collections import OrderedDict
from FusionCharts.fusioncharts import FusionCharts
from datetime import datetime
from django.db.models import Sum
from django.core.files.storage import default_storage


#######################################################################################################
def explore(request):
    hotel = Hotel.objects.all()
    meter = Meter.objects.all()
    context = {
        'Hotels': hotel ,
            }
            
    return render(request, 'app/explore.html', context=context)


#######################################################################################################
def dump_to_database():

    with open(os.path.join(settings.MEDIA_ROOT, 'CSVFiles', 'building_data.csv'), 'r') as f:
        reader = csv.reader(f)
        # This skips the first row of the CSV file.
        next(f)
        for row in reader:
            try:
                 _, created = Hotel.objects.get_or_create(
                    id = row[0],
                    name = row[1],
                    )
            except Exception as e:
                print('Error While creating object: ',e)      

    with open(os.path.join(settings.MEDIA_ROOT, 'CSVFiles', 'meter_data.csv'), 'r') as f:
        reader = csv.reader(f)
        # This skips the first row of the CSV file.
        next(f)
        for row in reader:
            try:
                _, created = Meter.objects.get_or_create(
                   building_id = Hotel.objects.get(id=row[0]),
                   id = row[1],
                   fuel = row[2],
                   unit = row[3]
                )
            except Exception as e:
                print('Error While creating object: ',e)      

    with open(os.path.join(settings.MEDIA_ROOT, 'CSVFiles', 'halfhourly_data.csv'), 'r') as f:
        reader = csv.DictReader(f)
        list_of_dict = list(reader)
        
        objs = [
            Consumption(
               consumption = row['ï»¿consumption'],
               meter_id = Meter.objects.get_or_create(id=row["meter_id"]),
               reading_date_time = row["reading_date_time"],
            )

        for row in list_of_dict
        ]
        try:
            msg = Consumption.objects.bulk_create(objs, batch_size=32, ignore_conflicts=True)
            returnmsg = {"status_code": 200}
            print('imported successfully', returnmsg)
        except Exception as e:
            returnmsg = {"status_code": 500}
            print('Error While Importing Data: ',e, returnmsg)


#######################################################################################################
def upload_csv(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        files = request.FILES.getlist('files')
        if form.is_valid():
                for f in files:
                    file_instance = UploadModel(files=f)
                    file_instance.save()
                if default_storage.exists(file_instance.files.path) == "False":
                    dump_to_database()
        return HttpResponseRedirect(reverse("explore"))

    else:
        form = UploadFileForm()
    return render(request, 'app/upload.html', {
        'form': form
    })


#######################################################################################################
def barchart(request, hotel_id):

    hotel = Hotel.objects.get(id=hotel_id)
    meter_info =  Consumption.objects.values('meter_id__fuel').annotate(Sum('consumption'))

    dataSource = {}
    dataSource['chart'] = { 
            "caption": f"Total Enegry Consumption by {hotel.name} Hotel",
            "subCaption": f"Consumption By Meter",
            "xAxisName": "Meter",
            "yAxisName": f" Usage (Kwh)",
            "numberPrefix": "",
            "theme": "zune"
        }
    dataSource['data'] = []

    for meter in meter_info:
        data = {}
        data['label'] = meter['meter_id__fuel']
        data['value'] = str(meter['consumption__sum'])
        dataSource['data'].append(data)    

       
        # Create an object for the Column 2D chart using the FusionCharts class constructor                      
    column2D = FusionCharts("column2D", "Candy" , "500", "450", "chart-1", "json", dataSource)
    return render(request, 'app/index.html', {'output': column2D.render()}) 



    