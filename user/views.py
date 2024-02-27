from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import make_password
# from .forms import ProfileForm, ChangePasswordForm
from django.utils.crypto import get_random_string
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from app.actions import GetData, GetMerakiData
from django.contrib import messages
from datetime import datetime
from app.models import *
User = get_user_model()
import requests


# Create your views here.
def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')
    
def home(request):
    if request.user.is_anonymous:
        return render(request, 'home.html')
    else:
        datas = Data.objects.all()
        last_data = Data.objects.order_by('-id').first()
        last_yield = last_data.Yield
        last_humidity = last_data.humidity
        last_wind_speed = last_data.wind_speed
        last_temperature = last_data.temperature
        last_precipitation = last_data.precipitation
        last_cultivated_areas = last_data.cultivated_areas
        
        context = {
            'datas': datas,
            'last_yield': last_yield,
            'last_humidity': last_humidity,
            'last_wind_speed': last_wind_speed,
            'last_temperature': last_temperature,
            'last_precipitation': last_precipitation,
            'last_cultivated_areas': last_cultivated_areas,
        }
        GetData()
        # GetMerakiData()
        return render(request, 'dashboard.html', context)


@login_required
def generate_api_key(request):
    user = request.user
    if request.method == 'POST':
        api_key = get_random_string(32, allowed_chars="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
        api_secret = get_random_string(64, allowed_chars="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
        user.api_key = api_key
        user.api_secret = make_password(api_secret)
        user.save()
        return render(request, 'api_keys.html', {'api_key': api_key, 'api_secret': api_secret})
    else:
        api_key = user.api_key
        api_secret = user.api_secret
        return render(request, 'api_keys.html', {'api_key': api_key, 'api_secret': api_secret})

# Edit Profile
@login_required
def profile(request):
    user = request.user

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if first_name and last_name and email:
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.save()
            messages.success(request, 'Profile information updated successfully.')

        if current_password and new_password and confirm_password:
            if user.check_password(current_password):
                if new_password == confirm_password:
                    user.set_password(new_password)
                    user.save()
                    update_session_auth_hash(request, user) 
                    messages.success(request, 'Password changed successfully.')
                else:
                    messages.error(request, 'New password and confirm password do not match.')
            else:
                messages.error(request, 'Current password is incorrect.')

        return redirect('/accounts/profile/')

    return render(request, 'profiles.html', {
        'user': user,
    })

###################################################################################################

import joblib
import pandas as pd
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def ussd(request):
    if request.method == 'GET':
        return HttpResponse("Welcome!")
    if request.method == 'POST':
        session_id = request.POST.get('sessionId')
        service_code = request.POST.get('serviceCode')
        phone_number = request.POST.get('phoneNumber')
        text = request.POST.get('text')

        response = ""

        if text == "":
            response = "CON RIM Agricole \n"
            response += "1. Sensors Data \n"
            response += "2. Weather Data \n"
            response += "3. Prediction \n"

        elif text == "1":
            response = "CON Select Sensor \n"
            response += "1. Sensor 1 \n"
            response += "2. Sensor 2 \n"
            response += "3. Sensor 3 "

        elif text == "1*1":
            response = "CON Choose Data \n"
            response += "1. Humidity \n"
            response += "2. Temperature \n"
           
        elif text == "1*1*1":
            last_data = Sensor1.objects.order_by('-id').first()
            humidity = last_data.humidity
            response = f"END The humidity is {humidity} %"
        elif text == "1*1*2":
            last_data = Sensor1.objects.order_by('-id').first()
            temperature = last_data.temperature
            response = f"END The temperature is {temperature} °C\n"

        elif text == "1*2":
            response = "CON Choose Data \n"
            response += "1. TVOC \n"
            response += "2. ECO2 \n"
            response += "3. Noise \n"
            response += "4. Humidity \n"
            response += "5. Temperature \n"
            response += "6. Air Quality \n"
        
        elif text == "1*2*1":
            last_data = Sensor2.objects.order_by('-id').first()
            tvoc = last_data.tvoc
            response = f"END The tvoc is {tvoc} µg/m³"
        elif text == "1*2*2":
            last_data = Sensor2.objects.order_by('-id').first()
            eco2 = last_data.eco2
            response = f"END The eco2 is {eco2} kg/m³"
        elif text == "1*2*3":
            last_data = Sensor2.objects.order_by('-id').first()
            noise = last_data.noise
            response = f"END The noise is {noise} dBA"
        elif text == "1*2*4":
            last_data = Sensor2.objects.order_by('-id').first()
            humidity = last_data.humidity
            response = f"END The humidity is {humidity} %"
        elif text == "1*2*5":
            last_data = Sensor2.objects.order_by('-id').first()
            temperature = last_data.temperature
            response = f"END The temperature is {temperature} °C"
        elif text == "1*2*6":
            last_data = Sensor2.objects.order_by('-id').first()
            air_quality = last_data.air_quality
            response = f"END The air quality is {air_quality} AQI"

        elif text == "1*3":
            response = "CON Choose Data \n"
            response += "1. TVOC \n"
            response += "2. ECO2 \n"
            response += "3. Noise \n"
            response += "4. Humidity \n"
            response += "5. Temperature \n"
            response += "6. Air Quality \n"
        
        elif text == "1*3*1":
            last_data = Sensor3.objects.order_by('-id').first()
            tvoc = last_data.tvoc
            response = f"END The Tvoc is {tvoc} µg/m³"
        elif text == "1*3*2":
            last_data = Sensor3.objects.order_by('-id').first()
            eco2 = last_data.eco2
            response = f"END The Eco2 is {eco2} kg/m³"
        elif text == "1*3*3":
            last_data = Sensor3.objects.order_by('-id').first()
            noise = last_data.noise
            response = f"END The noise is {noise} dBA"
        elif text == "1*3*4":
            last_data = Sensor3.objects.order_by('-id').first()
            humidity = last_data.humidity
            response = f"END The humidity is {humidity} %"
        elif text == "1*3*5":
            last_data = Sensor3.objects.order_by('-id').first()
            temperature = last_data.temperature
            response = f"END The temperature is {temperature} °C"
        elif text == "1*3*6":
            last_data = Sensor3.objects.order_by('-id').first()
            air_quality = last_data.air_quality
            response = f"END The air quality is {air_quality} AQI"

        elif text == "2":
            response = "CON Choose Data \n"
            response += "1. Humidity \n"
            response += "2. Wind Speed \n"
            response += "3. Temperature \n"
           
        elif text == "2*1":
            last_data = Data.objects.order_by('-id').first()
            humidity = last_data.humidity
            response = f"END The humidity is {humidity} %"
        elif text == "2*2":
            last_data = Data.objects.order_by('-id').first()
            wind_speed = last_data.wind_speed
            response = f"END The wind speed is {wind_speed} m/s"
        elif text == "2*3":
            last_data = Data.objects.order_by('-id').first()
            temperature = last_data.temperature
            response = f"END The temperature is {temperature} °C\n"
        
        elif text == "3":
            model = joblib.load('model.h5')
            data = Data.objects.order_by('-id')[:100]
            data = pd.DataFrame.from_records(data.values())
            data.sort_values('date', inplace=True)
            cumulative_data = data.copy()
            cumulative_data[['humidity', 'temperature', 'precipitation', 'wind_speed', 'cultivated_areas']] = data[['humidity', 'temperature', 'precipitation', 'wind_speed', 'cultivated_areas']].sum()
            features = ['humidity', 'temperature', 'precipitation', 'wind_speed', 'cultivated_areas']
            y_pred = model.predict(cumulative_data[features])[0]
            response = f"END The prediction yield is {y_pred} tons"

        return HttpResponse(response)