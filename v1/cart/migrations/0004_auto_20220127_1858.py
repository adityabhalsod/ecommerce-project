# Generated by Django 3.0.8 on 2022-01-27 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cart", "0003_auto_20220127_1831"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cart",
            name="is_lock",
            field=models.BooleanField(default=False),
        ),
    ]
