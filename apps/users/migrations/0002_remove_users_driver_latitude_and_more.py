# Generated by Django 5.0.2 on 2024-04-21 07:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='driver_latitude',
        ),
        migrations.RemoveField(
            model_name='users',
            name='driver_longitude',
        ),
        migrations.RemoveField(
            model_name='users',
            name='user_type',
        ),
    ]
