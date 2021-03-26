from django.contrib import admin
from .models import Hotel, UploadModel, Meter, Consumption

admin.site.register(Hotel)
admin.site.register(UploadModel)
admin.site.register(Meter)
admin.site.register(Consumption)

