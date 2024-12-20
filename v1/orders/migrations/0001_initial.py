# Generated by Django 3.0.8 on 2022-01-16 19:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("delivery", "0008_auto_20220115_1220"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("updated_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("is_deleted", models.BooleanField(default=False)),
                (
                    "order_number",
                    models.CharField(blank=True, default="", max_length=255, null=True),
                ),
                ("order_date", models.DateTimeField(default=django.utils.timezone.now)),
                ("delivery_time_start", models.TimeField(blank=True, null=True)),
                ("delivery_time_end", models.TimeField(blank=True, null=True)),
                (
                    "package_size",
                    models.CharField(blank=True, default="", max_length=255, null=True),
                ),
                ("total_amount", models.FloatField(blank=True, default=0.0, null=True)),
                ("discount", models.FloatField(blank=True, default=0.0, null=True)),
                ("tax", models.FloatField(blank=True, default=0.0, null=True)),
                (
                    "total_quantity",
                    models.IntegerField(blank=True, default=0, null=True),
                ),
                (
                    "order_status",
                    models.CharField(
                        choices=[
                            ("order_confirm", "Order confirm"),
                            ("order_packing", "Order packing"),
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
                (
                    "order_type",
                    models.CharField(
                        choices=[
                            ("cash_on_delivery", "Cash on delivery"),
                            ("online", "Online"),
                            ("not_attempt", "Not attempt"),
                        ],
                        default="not_attempt",
                        max_length=255,
                    ),
                ),
                (
                    "refund_method",
                    models.CharField(
                        choices=[
                            ("bank_account", "Bank account"),
                            ("wallet_amount", "Wallet amount"),
                            ("online", "Online"),
                            ("not_attempt", "Not attempt"),
                        ],
                        default="not_attempt",
                        max_length=255,
                    ),
                ),
                (
                    "refund_status",
                    models.CharField(
                        choices=[
                            ("successful", "Successful"),
                            ("failed", "Failed"),
                            ("in_progress", "In progress"),
                            ("not_attempt", "Not attempt"),
                        ],
                        default="not_attempt",
                        max_length=255,
                    ),
                ),
                (
                    "customer",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="customer",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "delivery_boy",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="order_delivered",
                        to="delivery.DeliveryBoy",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
