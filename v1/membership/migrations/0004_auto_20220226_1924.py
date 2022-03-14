# Generated by Django 3.1.14 on 2022-02-26 19:24

from django.conf import settings
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("membership", "0003_auto_20220205_1102"),
    ]

    operations = [
        migrations.CreateModel(
            name="MembershipBenefits",
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
                ("text", models.TextField(blank=True, default="", null=True)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="MembershipPlain",
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
                    "type",
                    models.CharField(
                        choices=[
                            ("one_month", "One month"),
                            ("three_month", "Three month"),
                            ("half_year", "Half year"),
                            ("one_year", "One year"),
                            ("not_attempt", "Not attempt"),
                        ],
                        default="one_month",
                        max_length=255,
                    ),
                ),
                ("mrp_amount", models.FloatField(blank=True, default=0.0, null=True)),
                (
                    "discount_amount",
                    models.FloatField(blank=True, default=0.0, null=True),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.RenameField(
            model_name="membership",
            old_name="fee",
            new_name="amount",
        ),
        migrations.AlterUniqueTogether(
            name="membership",
            unique_together={("customer", "start_at", "end_at")},
        ),
        migrations.RemoveField(
            model_name="membership",
            name="type",
        ),
    ]
