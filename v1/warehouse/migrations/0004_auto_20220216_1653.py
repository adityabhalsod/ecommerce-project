# Generated by Django 3.0.8 on 2022-02-16 16:53

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("warehouse", "0003_auto_20220216_1648"),
    ]

    operations = [
        migrations.CreateModel(
            name="Supplier",
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
                    "business_name",
                    models.CharField(blank=True, default="", max_length=255, null=True),
                ),
                (
                    "mobile",
                    models.CharField(blank=True, default="", max_length=255, null=True),
                ),
                (
                    "email",
                    models.CharField(blank=True, default="", max_length=255, null=True),
                ),
                (
                    "gst_number",
                    models.CharField(blank=True, default="", max_length=255, null=True),
                ),
                ("address", models.TextField(blank=True, default="", null=True)),
                (
                    "city",
                    models.CharField(blank=True, default="", max_length=64, null=True),
                ),
                (
                    "state",
                    models.CharField(blank=True, default="", max_length=25, null=True),
                ),
                (
                    "country",
                    models.CharField(blank=True, default="", max_length=25, null=True),
                ),
                (
                    "pin_code",
                    models.CharField(blank=True, default="", max_length=16, null=True),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AlterField(
            model_name="warehouse",
            name="address",
            field=models.TextField(blank=True, default="", null=True),
        ),
        migrations.AlterField(
            model_name="warehouse",
            name="city",
            field=models.CharField(blank=True, default="", max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name="warehouse",
            name="country",
            field=models.CharField(blank=True, default="", max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name="warehouse",
            name="pin_code",
            field=models.CharField(blank=True, default="", max_length=16, null=True),
        ),
        migrations.AlterField(
            model_name="warehouse",
            name="state",
            field=models.CharField(blank=True, default="", max_length=25, null=True),
        ),
    ]
