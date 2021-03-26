from django.contrib import admin 
from django.urls import path 
from django.conf import settings 
from django.conf.urls.static import static 
from . import views

urlpatterns = [
      path("", views.upload_csv, name="upload_view"),
      path("explore/", views.explore, name="explore"),
      path("explore/<str:hotel_id>", views.barchart, name="barchart"),
]