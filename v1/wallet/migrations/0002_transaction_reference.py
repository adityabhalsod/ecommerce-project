# Generated by Django 3.0.8 on 2022-02-13 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("wallet", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="transaction",
            name="reference",
            field=models.CharField(blank=True, default="", max_length=255, null=True),
        ),
    ]
