# Generated by Django 4.1 on 2023-07-20 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_image_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='photo',
            field=models.ImageField(upload_to='images/'),
        ),
    ]
