import requests
import threading
import pandas as pd
import seaborn as sns
from app.models import *
import plotly.express as px
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from django.http import JsonResponse
from datetime import datetime, timedelta
from sklearn.preprocessing import StandardScaler

def GetData():
    print('Creating Sensor Data...')
    api_key = 'put your openweathermap API Key'
    city = 'The city which you want to retrive its data'
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&APPID={api_key}"

    try:
        response = requests.get(url)
        response.raise_for_status() 
        weather_data = response.json()
        temperature = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        wind_speed = weather_data['wind']['speed']
        data = Data.objects.create(humidity=humidity, wind_speed=wind_speed, temperature=temperature, cultivated_areas=1000)
        data.save()
    except requests.exceptions.RequestException as e:
        print("Failed to fetch weather data")

def GetMerakiData():
    print('Creating Sensor Data...')
    header = {'Authorization': 'Bearer Your Meraki API Key'}
    url = "https://api.meraki.com/api/v1/organizations/your_organisation_id/sensor/readings/latest"
    try:
        response = requests.get(url, headers=header)
        data = response.json()
    except requests.exceptions.RequestException as e:
        print("Failed to fetch weather data")

def get_latest_data(request):
    datas = Data.objects.all()
    last_data = Data.objects.order_by('-id').first()
    last_yield = last_data.Yield
    last_humidity = last_data.humidity
    last_wind_speed = last_data.wind_speed
    last_temperature = last_data.temperature
    last_precipitation = last_data.precipitation
    last_cultivated_areas = last_data.cultivated_areas

    data = {
        # 'datas': datas,
        'last_yield': last_yield,
        'last_humidity': last_humidity,
        'last_wind_speed': last_wind_speed,
        'last_temperature': last_temperature,
        'last_precipitation': last_precipitation,
        'last_cultivated_areas': last_cultivated_areas,
    }
    GetData()
    # GetMerakiData()
    return JsonResponse(data)


def data_analysis(request):
    # Load the data from the Sensor3 model
    sensor_data = Sensor3.objects.all()
    data = pd.DataFrame(list(sensor_data.values()))
    data['date'] = pd.to_datetime(data['date'])
    data.set_index('date', inplace=True)
    # normalize the data using min-max normalization
    data_normalized = (data - data.min()) / (data.max() - data.min())
    
    # Decomposition - Trend
    plt.figure(figsize=(8, 5))
    res_tvoc = seasonal_decompose(data_normalized['tvoc'], model='additive', period=5)
    res_eco2 = seasonal_decompose(data_normalized['eco2'], model='additive', period=5)
    res_noise = seasonal_decompose(data_normalized['noise'], model='additive', period=5)
    res_humidity = seasonal_decompose(data_normalized['humidity'], model='additive', period=5)
    res_temperature = seasonal_decompose(data_normalized['temperature'], model='additive', period=5)
    res_indoorAirQuality = seasonal_decompose(data_normalized['indoorAirQuality'], model='additive', period=5)

    plt.plot(res_tvoc.trend, label="Tvoc")
    plt.plot(res_eco2.trend, label="Eco2")
    plt.plot(res_noise.trend, label="Noise")
    plt.plot(res_humidity.trend, label="Humidity")
    plt.plot(res_temperature.trend, label="Temperature")
    plt.plot(res_indoorAirQuality.trend, label="AirQuality")
    
    plt.legend()
    plt.xlabel('Time')
    plt.ylabel('Trend')
    plt.title('Variable Trend')
    plt.savefig('graphe_trend.png')
    plt.close()

    # Decomposition - Seasonality
    plt.figure(figsize=(8, 5))
    plt.plot(res_tvoc.seasonal, label="Tvoc")
    plt.plot(res_eco2.seasonal, label="Eco2")
    plt.plot(res_noise.seasonal, label="Noise")
    plt.plot(res_humidity.seasonal, label="Humidity")
    plt.plot(res_temperature.seasonal, label="Temperature")
    plt.plot(res_indoorAirQuality.seasonal, label="AirQuality")

    plt.legend()
    plt.xlabel('Time')
    plt.ylabel('Seasonality')
    plt.title('Decomposition - Seasonality')
    plt.savefig('seasonality.png')
    plt.close()

    # Decomposition - Noise
    plt.figure(figsize=(8, 5))
    plt.plot(res_tvoc.resid, label="Tvoc")
    plt.plot(res_eco2.resid, label="Eco2")
    plt.plot(res_noise.resid, label="Noise")
    plt.plot(res_humidity.resid, label="Humidity")
    plt.plot(res_temperature.resid, label="Temperature")
    plt.plot(res_indoorAirQuality.resid, label="AirQuality")
    plt.legend()
    plt.xlabel('Time')
    plt.ylabel('Noise')
    plt.title('Decomposition - Noise')
    plt.savefig('decomposition_noise.png')
    plt.close()

    # Initial Values
    plt.figure(figsize=(8, 5))
    plt.plot(data_normalized['tvoc'], label="Tvoc")
    plt.plot(data_normalized['eco2'], label="Eco2")
    plt.plot(data_normalized['noise'], label="Noise")
    plt.plot(data_normalized['humidity'], label="Humidity")
    plt.plot(data_normalized['temperature'], label="Temperature")
    plt.plot(data_normalized['indoorAirQuality'], label="AirQuality")

    plt.legend()
    plt.xlabel('Time')
    plt.ylabel('Initial Values')
    plt.title('Initial Values')
    plt.savefig('initial_values.png')
    plt.close()

    # Clustering
    clustering_data = data_normalized[['tvoc', 'eco2', 'noise', 'humidity', 'temperature', 'indoorAirQuality']]
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(clustering_data)
    dbscan = DBSCAN(eps=0.5, min_samples=5)
    clusters = dbscan.fit_predict(scaled_data)

    # Generate and save the correlation matrix image
    variables = ['tvoc', 'eco2', 'noise', 'humidity', 'temperature', 'indoorAirQuality']
    corr_matrix = data_normalized[variables].corr()

    plt.figure(figsize=(8, 6))
    colors = ['#4a86e8', '#3f9c35', '#e83b3b', '#f09c1c', '#a536a5']
    cmap = sns.color_palette(colors)
    sns.heatmap(corr_matrix, annot=True, cmap=cmap, fmt=".2f", linewidths=0.8)
    plt.title('Correlation Matrix of Variables')
    plt.savefig('matrix.png')
    plt.close()

    # Generate and save the clusters plot
    fig = plt.figure(figsize=(5, 2))
    df = data
    fig = px.scatter(df, x="humidity", y="temperature", color=clusters, size='tvoc', hover_data=['indoorAirQuality'])
    fig.write_image('clusters_plot.png')

    # Prepare the context to pass to the template
    context = {
        'trend_img': 'graphe_tendance.png',
        'seasonality_img': 'decomposition_seasonality.png',
        'noise_img': 'decomposition_noise.png',
        'initial_values_img': 'initial_values.png',
        'corr_matrix_img': 'correlation_matrix.png',
        'clusters_img': 'clusters_plot.png'
    }

    return render(request, 'data_analysis.html', context)
