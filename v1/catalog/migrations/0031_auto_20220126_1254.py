# Generated by Django 3.0.8 on 2022-01-26 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0030_auto_20220126_1057"),
    ]

    operations = [
        migrations.AlterField(
            model_name="variation",
            name="value",
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
    ]
