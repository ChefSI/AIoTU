from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password
from django.utils.crypto import get_random_string
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render
from rest_framework import status
from datetime import datetime
from .serializers import *
from app.models import *
from user.models import User
import pandas as pd
import joblib

# create your views here
class PredictionAPIView(APIView):
    
    def get(self, request):
        api_key = request.headers.get('AIoTU')
        if not api_key:
            return Response({"error": "API key is missing"}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            user = User.objects.get(api_key=api_key)
        except User.DoesNotExist:
            return Response({"error": "Invalid API key"}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            model = joblib.load('model.h5')
            data = Data.objects.order_by('-id')[:90]
            # data = Data.objects.all()
            data = pd.DataFrame.from_records(data.values())
            data.sort_values('date', inplace=True)
            cumulative_data = data.copy()
            cumulative_data[['humidity', 'temperature', 'precipitation', 'wind_speed', 'cultivated_areas']] = data[['humidity', 'temperature', 'precipitation', 'wind_speed', 'cultivated_areas']].sum()
            features = ['humidity', 'temperature', 'precipitation', 'wind_speed', 'cultivated_areas']
            y_pred = model.predict(cumulative_data[features])[0]
            
            response_data = {
                'prediction': y_pred
            }
            return Response(response_data)

        except ValueError:
            return Response({'error': 'Invalid date format. Use dd/mm/yyyy.'}, status=status.HTTP_400_BAD_REQUEST)


class SensorDataAPIView(APIView):
    def get(self, request, sensor_number):
        api_key = request.headers.get('AIoTU')
        if not api_key:
            return Response({"error": "API key is missing"}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            user = User.objects.get(api_key=api_key)
        except User.DoesNotExist:
            return Response({"error": "Invalid API key"}, status=status.HTTP_401_UNAUTHORIZED)
        if sensor_number==1:
            last_record = Sensor1.objects.latest('id')
            serializer = Sensor1Serializer(last_record)
            return Response(serializer.data)
        elif sensor_number==2:
            last_record = Sensor2.objects.latest('id')
            serializer = Sensor2Serializer(last_record)
            return Response(serializer.data)
        elif sensor_number==3:
            last_record = Sensor3.objects.latest('id')
            serializer = Sensor3Serializer(last_record)
            return Response(serializer.data)
        else:
            last_record = Data.objects.latest('id')
            serializer = DataSerializer(last_record)
            return Response(serializer.data)


class APIKeysView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = User.objects.get(email=request.user.email)
        if user:
            return Response(data={"api_key": user.api_key}, status=status.HTTP_200_OK)

    def post(self, request):
        user = User.objects.get(email=request.user.email)
        if user:
            api_key = get_random_string(
                32, allowed_chars="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
            api_secret = get_random_string(
                64, allowed_chars="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
            user.api_key = api_key
            user.api_secret = make_password(api_secret)
            user.save()
            return Response(data={"api_key": api_key, "api_secret": api_secret}, status=status.HTTP_200_OK)


class ValidateAPIKeysView(APIView):
    def post(self, request):
        api_key = request.headers.get("api-key")
        api_secret = request.headers.get("api-secret")

        try:
            user = User.objects.get(api_key=api_key)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if user:
            if user.api_key == api_key and user.has_valid_api_secret(api_secret):
                return Response(data={"valid": True}, status=status.HTTP_200_OK)
            return Response(data={"valid": False}, status=status.HTTP_200_OK)