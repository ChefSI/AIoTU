# Generated by Django 4.1 on 2023-07-22 23:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_alter_sensor1_date_alter_sensor2_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensor3',
            name='date',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]
