# Generated by Django 3.0.8 on 2022-02-05 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0011_order_no_contact_delivery"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="delivery_boy_tip",
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
    ]
