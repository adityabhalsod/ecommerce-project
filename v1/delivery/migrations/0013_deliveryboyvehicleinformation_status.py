# Generated by Django 3.0.8 on 2022-02-05 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("delivery", "0012_auto_20220205_2128"),
    ]

    operations = [
        migrations.AddField(
            model_name="deliveryboyvehicleinformation",
            name="status",
            field=models.CharField(
                choices=[
                    ("approve", "Approve"),
                    ("reject", "Reject"),
                    ("pending", "Pending"),
                ],
                default="pending",
                max_length=255,
            ),
        ),
    ]
