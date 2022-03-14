# Generated by Django 3.0.8 on 2022-02-05 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0020_order_membership_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="final_membership_fee",
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
    ]
