# Generated by Django 3.0.8 on 2022-01-09 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="address",
            name="is_billing",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="address",
            name="is_shipping",
            field=models.BooleanField(default=False),
        ),
    ]
