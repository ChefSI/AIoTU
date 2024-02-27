from rest_framework import serializers
from app.models import *

class SensorDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorData
        exclude =("date", "id",)

class Sensor1Serializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor1
        exclude =("date", "id",)

class Sensor2Serializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor2
        exclude =("date", "id",)

class Sensor3Serializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor3
        exclude =("date", "id",)

class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Data
        exclude =("date", "id", "cultivated_areas", "Yield")