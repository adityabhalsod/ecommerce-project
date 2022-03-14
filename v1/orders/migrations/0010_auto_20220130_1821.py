# Generated by Django 3.0.8 on 2022-01-30 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0009_auto_20220130_1738"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="order_status",
            field=models.CharField(
                choices=[
                    ("order_awaiting_for_payment", "Order awaiting for payment"),
                    ("order_placed", "Order Placed"),
                    ("order_packing_starting", "Order packing starting"),
                    ("order_packing_completed", "Order packing completed"),
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
