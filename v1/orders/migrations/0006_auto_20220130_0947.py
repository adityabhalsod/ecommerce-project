# Generated by Django 3.0.8 on 2022-01-30 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0005_order_sequence"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="order_status",
            field=models.CharField(
                choices=[
                    ("order_confirm", "Order confirm"),
                    ("order_packing", "Order packing"),
                    ("order_pickup", "Order pickup"),
                    ("order_on_the_way", "Order on the way"),
                    ("order_delivery", "Order delivered"),
                    ("order_failed", "Order failed"),
                    ("order_cancel", "Order cancel"),
                    ("not_attempt", "Not attempt"),
                ],
                default="not_attempt",
                max_length=255,
            ),
        ),
    ]
