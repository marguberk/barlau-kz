# Generated by Django 5.1.6 on 2025-05-03 10:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('logistics', '0007_vehicle_cargo_capacity_vehicle_chassis_number_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vehiclemaintenance',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='vehiclemaintenance',
            name='vehicle',
        ),
        migrations.RemoveField(
            model_name='vehiclephoto',
            name='uploaded_by',
        ),
        migrations.RemoveField(
            model_name='vehiclephoto',
            name='vehicle',
        ),
        migrations.RemoveField(
            model_name='vehicle',
            name='cargo_capacity',
        ),
        migrations.RemoveField(
            model_name='vehicle',
            name='chassis_number',
        ),
        migrations.RemoveField(
            model_name='vehicle',
            name='engine_capacity',
        ),
        migrations.RemoveField(
            model_name='vehicle',
            name='engine_number',
        ),
        migrations.RemoveField(
            model_name='vehicle',
            name='fuel_type',
        ),
        migrations.RemoveField(
            model_name='vehicle',
            name='height',
        ),
        migrations.RemoveField(
            model_name='vehicle',
            name='length',
        ),
        migrations.RemoveField(
            model_name='vehicle',
            name='max_weight',
        ),
        migrations.RemoveField(
            model_name='vehicle',
            name='vin_number',
        ),
        migrations.RemoveField(
            model_name='vehicle',
            name='width',
        ),
        migrations.DeleteModel(
            name='VehicleDocument',
        ),
        migrations.DeleteModel(
            name='VehicleMaintenance',
        ),
        migrations.DeleteModel(
            name='VehiclePhoto',
        ),
    ]
