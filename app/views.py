from django.contrib.auth.decorators import login_required
from statsmodels.tsa.seasonal import seasonal_decompose
from sklearn.ensemble import RandomForestRegressor
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render
import matplotlib.pyplot as plt
from io import BytesIO
import urllib.request
from user.views import *
from .actions import *
from .models import *
from time import time
import pandas as pd
import requests
import base64
import random
import time
import json
import csv


# Create your views here.
@login_required()
def Camera(request):
    return render(request, 'camera.html')

@login_required
def sensor1(request):
    datas = Sensor1.objects.all()
    last_data = Sensor1.objects.order_by('-id').first()
    last_humidity = last_data.humidity
    last_temperature = last_data.temperature
    
    context = {
        'datas': datas,
        'last_humidity': last_humidity,
        'last_temperature': last_temperature,
    }

    return render(request, 'sensor1.html', context)

@login_required
def sensor2(request):
    datas = Sensor2.objects.all()
    last_data = Sensor2.objects.order_by('-id').first()
    last_tvoc = last_data.tvoc
    last_eco2 = last_data.eco2
    last_noise = last_data.noise
    last_humidity = last_data.humidity
    last_temperature = last_data.temperature
    last_air_quality = last_data.air_quality
    
    context = {
        'datas': datas,
        'last_tvoc': last_tvoc,
        'last_eco2': last_eco2,
        'last_noise': last_noise,
        'last_humidity': last_humidity,
        'last_temperature': last_temperature,
        'last_air_quality': last_air_quality,
    }
    
    return render(request, 'sensor2.html', context)

@login_required
def sensor3(request):
    datas = Sensor3.objects.all()
    last_data = Sensor3.objects.order_by('-id').first()
    last_tvoc = last_data.tvoc
    last_eco2 = last_data.eco2
    last_noise = last_data.noise
    last_humidity = last_data.humidity
    last_temperature = last_data.temperature
    last_air_quality = last_data.air_quality
    
    context = {
        'datas': datas,
        'last_tvoc': last_tvoc,
        'last_eco2': last_eco2,
        'last_noise': last_noise,
        'last_humidity': last_humidity,
        'last_temperature': last_temperature,
        'last_air_quality': last_air_quality,
    }
   
    return render(request, 'sensor3.html', context)

def gallery(request):
    images = Image.objects.all()
    return render(request, 'gallery.html', {'images': images})



import joblib
import pandas as pd
from django.shortcuts import render
from django.contrib import messages

@login_required
def prediction(request):
    # Load the model
    model = joblib.load('model.h5')
    data = Data.objects.order_by('-id')[:100]
    # Convert the QuerySet to a pandas DataFrame
    data = pd.DataFrame.from_records(data.values())
    # Sort the data by date
    data.sort_values('date', inplace=True)
    # Calculate the cumulative sum of yield and climate features
    cumulative_data = data.copy()
    cumulative_data[['humidity', 'temperature', 'precipitation', 'wind_speed', 'cultivated_areas']] = data[['humidity', 'temperature', 'precipitation', 'wind_speed', 'cultivated_areas']].sum()
    features = ['humidity', 'temperature', 'precipitation', 'wind_speed', 'cultivated_areas']
    y_pred = model.predict(cumulative_data[features])[0]

    context = {
        'prediction': y_pred
    }
    return render(request, 'prediction.html', context)
