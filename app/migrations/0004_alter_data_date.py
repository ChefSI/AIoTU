# Generated by Django 4.1 on 2023-07-10 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_rename_acquisition_date_image_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
    ]