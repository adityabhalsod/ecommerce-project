# Generated by Django 3.0.8 on 2022-02-17 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("promotion", "0005_auto_20220217_1748"),
    ]

    operations = [
        migrations.AlterField(
            model_name="discountvoucher",
            name="value_type",
            field=models.CharField(
                choices=[("fixed", "Fixed (Rs.)"), ("percentage", "Percentage (%)")],
                default="fixed",
                max_length=10,
            ),
        ),
    ]
