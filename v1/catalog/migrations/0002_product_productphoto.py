# Generated by Django 3.0.8 on 2022-01-12 18:10

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Product",
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
                    "item_code",
                    models.CharField(blank=True, default="", max_length=255, null=True),
                ),
                (
                    "item_name",
                    models.CharField(blank=True, default="", max_length=255, null=True),
                ),
                (
                    "bill_display_item_name",
                    models.CharField(blank=True, default="", max_length=255, null=True),
                ),
                ("short_description", models.TextField(default="")),
                ("long_description", models.TextField(default="")),
                (
                    "hsn_code",
                    models.CharField(blank=True, default="", max_length=255, null=True),
                ),
                ("search_keyword", models.TextField(default="")),
                (
                    "slug",
                    models.CharField(blank=True, default="", max_length=255, null=True),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ProductPhoto",
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
                ("original", models.ImageField(blank=True, null=True, upload_to="")),
                ("webp_image", models.ImageField(blank=True, null=True, upload_to="")),
                ("thumbnail", models.ImageField(blank=True, null=True, upload_to="")),
                ("alt_text", models.TextField(default="")),
                ("is_default", models.BooleanField(default=False)),
                (
                    "product",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="catalog.Product",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
