from django.db import models

# Create your models here.
class Data(models.Model):
    date = models.DateField(auto_now_add=True)
    Yield = models.FloatField(default=0.0)
    humidity = models.FloatField(default=0.0)
    wind_speed = models.FloatField(default=0.0)
    temperature = models.FloatField(default=0.0)
    precipitation = models.FloatField(default=0.0)
    cultivated_areas = models.FloatField(default=0.0)

    def __str__(self):
        return self.date.strftime('%Y-%m-%d')


class SensorData(models.Model):
    tvoc = models.IntegerField()
    eco2 = models.IntegerField()
    noise = models.IntegerField()
    humidity = models.FloatField()
    temperature = models.FloatField()
    air_quality = models.IntegerField()
    date = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return f"{self.temperature}C, {self.humidity}%"

class Sensor1(models.Model):
    humidity = models.FloatField()
    temperature = models.FloatField()
    date = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return f"{self.temperature}C, {self.humidity}%"


class Sensor2(models.Model):
    tvoc = models.IntegerField()
    eco2 = models.IntegerField()
    noise = models.IntegerField()
    humidity = models.FloatField()
    temperature = models.FloatField()
    air_quality = models.IntegerField()
    date = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return f"{self.temperature}C, {self.humidity}%"


class Sensor3(models.Model):
    tvoc = models.IntegerField()
    eco2 = models.IntegerField()
    noise = models.IntegerField()
    humidity = models.FloatField()
    temperature = models.FloatField()
    air_quality = models.IntegerField()
    date = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return f"{self.temperature}C, {self.humidity}%"


class Image(models.Model):
    photo = models.ImageField(upload_to="images/")
    date = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.date

class Device(models.Model):
    serial = models.CharField(max_length=30, unique=True)
    mac = models.CharField(max_length=30, unique=True)
    model = models.CharField(max_length=10)

    def __str__(self):
        return self.serial