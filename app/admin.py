from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ["photo", "date"]

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ["serial", "mac", "model"]

@admin.register(Sensor1)
class Sensor1Admin(admin.ModelAdmin):
    list_display = ["humidity", "temperature", "date"]

@admin.register(Sensor2)
class Sensor2Admin(admin.ModelAdmin):
    list_display = ["tvoc", "eco2", "noise", "humidity", "temperature", "air_quality", "date"]

@admin.register(Sensor3)
class Sensor3Admin(admin.ModelAdmin):
    list_display = ["tvoc", "eco2", "noise", "humidity", "temperature", "air_quality", "date"]

@admin.register(SensorData)
class SensorDataAdmin(admin.ModelAdmin):
    list_display = ["tvoc", "eco2", "noise", "humidity", "temperature", "air_quality", "date"]

@admin.register(Data)
class DataAdmin(admin.ModelAdmin):
    list_display = ["date", "Yield", "humidity", "wind_speed", "temperature", "precipitation", "cultivated_areas"]