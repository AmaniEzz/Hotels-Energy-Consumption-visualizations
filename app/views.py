from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import UploadFileForm
from .models import UploadModel
from django.views.generic import CreateView, DetailView, ListView
from .models import Meter, Hotel, Consumption, UploadModel
from django.conf import settings
from django.contrib import messages
import os, csv
from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Sum
from django.core.files.storage import default_storage
from django.core.exceptions import ValidationError
from FusionCharts.fusioncharts import FusionCharts


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
            #progress_recorder.set_progress(i + 1, 100, f'On iteration {i}')

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
               meter_id = Meter.objects.get(id=row["meter_id"]),
               reading_date_time = row["reading_date_time"],
            )
        for row in list_of_dict
        ]
        try:
            msg = Consumption.objects.bulk_create(objs)
            returnmsg = {"status_code": 200}
            print('imported successfully', returnmsg)
        except Exception as e:
            returnmsg = {"status_code": 500}
            print('Error While Importing Data: ',e, returnmsg)


#######################################################################################################
def explore(request):

    hotels =  Hotel.objects.all()
    context = {
        'Hotels': hotels,
            }
            
    return render(request, 'app/explore.html', context=context)

#######################################################################################################
def upload_csv(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        files = request.FILES.getlist('filename')
        if form.is_valid():
            for f in files:
                if str(f).endswith('.csv'):
                    file, created = UploadModel.objects.get_or_create(filename=f)
                else:
                    messages.add_message(request, messages.ERROR, "Must be a CSV file")
                    return render(request, 'app/upload.html', {'form': form} )
            dump_to_database()
            return HttpResponseRedirect(reverse("explore"))

    else:
        form = UploadFileForm()
    return render(request, 'app/upload.html', {'form': form })

from django.db import connection

#######################################################################################################
def barchart(request, hotel_id):

    sql = ' SELECT sum(consumption),fuel, app_hotel.name \
            FROM public.app_consumption \
            left join app_meter ON app_consumption.meter_id_id = app_meter.id \
            left join app_hotel ON app_hotel.id = app_meter.building_id_id \
            group by app_hotel.name, fuel \
            order by app_hotel.name, sum(consumption)'
    
    cursor = connection.cursor()
    try:
        cursor.execute(sql, ['localhost'])
        row = cursor.fetchall()
        #print(row)
    except Exception as e:
        cursor.close

    hotel = Hotel.objects.get(id=hotel_id)

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

    for h in row:
        if h[2] == hotel.name:
            data = {}
            data['label'] = h[1]
            data['value'] = str(h[0])
            dataSource['data'].append(data)    

       
        # Create an object for the Column 2D chart using the FusionCharts class constructor                      
    column2D = FusionCharts("column2D", "Candy" , "500", "450", "chart-1", "json", dataSource)
    return render(request, 'app/index.html', {'output': column2D.render()}) 



    