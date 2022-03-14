# Generated by Django 3.0.8 on 2022-02-05 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cart", "0014_checkout_delivery_boy_tip"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="cart",
            name="rate",
        ),
        migrations.AddField(
            model_name="checkout",
            name="is_membership_exist",
            field=models.BooleanField(default=False),
        ),
    ]
