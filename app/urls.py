from django.urls import path
from .actions import *
from . import views

urlpatterns = [
    path('camera/', views.Camera, name='camera'),
    path('gallery/', views.gallery, name='gallery'),
    path('sensor/1/', views.sensor1, name='sensor1'),
    path('sensor/2/', views.sensor2, name='sensor2'),
    path('sensor/3/', views.sensor3, name='sensor3'),
    path('prediction/', views.prediction, name='prediction'),
    path('data/analysis/', data_analysis, name='data_analysis'),
]