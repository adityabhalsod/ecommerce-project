# Generated by Django 3.0.8 on 2022-01-12 18:17

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0001_initial"),
        ("catalog", "0002_product_productphoto"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProductStockMaster",
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
                ("mrp", models.FloatField(blank=True, default=0.0, null=True)),
                ("our_rate", models.FloatField(blank=True, default=0.0, null=True)),
                ("member_rate", models.FloatField(blank=True, default=0.0, null=True)),
                (
                    "purchase_rate",
                    models.FloatField(blank=True, default=0.0, null=True),
                ),
                (
                    "exclusive_rate",
                    models.FloatField(blank=True, default=0.0, null=True),
                ),
                ("discount", models.FloatField(blank=True, default=0.0, null=True)),
                ("is_exclusive_item", models.BooleanField(default=False)),
                ("is_super_saving_item", models.BooleanField(default=False)),
                ("is_free_delivery", models.BooleanField(default=False)),
                ("one_rs_store", models.BooleanField(default=False)),
                ("is_active_item", models.BooleanField(default=False)),
                ("max_order_quantity", models.IntegerField(default=0)),
                ("open_stock", models.IntegerField(default=0)),
                ("min_stock", models.IntegerField(default=0)),
                (
                    "product",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="catalog.Product",
                    ),
                ),
                (
                    "store",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="store.Store",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
