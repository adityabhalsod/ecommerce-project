# Generated by Django 3.0.8 on 2022-02-05 20:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("cart", "0020_checkout_final_membership_fee"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("catalog", "0045_auto_20220205_1155"),
        ("store", "0005_auto_20220130_0908"),
        ("orders", "0021_order_final_membership_fee"),
    ]

    operations = [
        migrations.CreateModel(
            name="FinalDeliveredOrder",
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
                ("rate", models.FloatField(blank=True, default=0.0, null=True)),
                (
                    "quantity",
                    models.PositiveIntegerField(blank=True, default=1, null=True),
                ),
                (
                    "checkout",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="checkout_delivered_order",
                        to="cart.Checkout",
                    ),
                ),
                (
                    "customer",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="customer_delivered_order",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "order",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="final_delivered_order",
                        to="orders.Order",
                    ),
                ),
                (
                    "product_variation",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="product_variation_delivered_order",
                        to="catalog.Variation",
                    ),
                ),
                (
                    "store",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="store_order_delivered_order",
                        to="store.Store",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
