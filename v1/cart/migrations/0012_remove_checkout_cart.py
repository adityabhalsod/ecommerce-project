# Generated by Django 3.0.8 on 2022-01-31 17:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("cart", "0011_checkout_final_quantity"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="checkout",
            name="cart",
        ),
    ]
