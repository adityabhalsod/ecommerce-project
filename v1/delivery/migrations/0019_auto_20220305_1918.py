# Generated by Django 3.1.14 on 2022-03-05 19:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("delivery", "0018_remove_deliveryboy_current_location"),
    ]

    operations = [
        migrations.RenameField(
            model_name="deliveryboyvehicleinformation",
            old_name="vehicle_license_number",
            new_name="vehicle_number",
        ),
    ]
